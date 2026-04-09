import pygame
import numpy as np

from Classes.Core.Renderer.Light import Light
from conf import TILE_SIZE, ERROR_TEXTURE





class Texture:
  def __init__(self, texture_path: str, normal_texture_path: str = "", size: np.ndarray[int] = np.array([1, 1], dtype=int)):
    self._texture_path: str = texture_path
    self._normal_texture_path: str = normal_texture_path
    self._size: np.ndarray[int] = size
    self._texture: pygame.Surface = None
    self.lit_surface: pygame.Surface = None
    self._normal_map: pygame.Surface = None
    self._last_pos = None


  def precomputeLight(self, render_pos: np.ndarray[int], light: np.ndarray[Light]):
    self._applyLighting(render_pos, light)


  def setSize(self, size: np.ndarray[int]) -> None:
    self._size = size
    transform_size = (self._size[0] * TILE_SIZE, self._size[1] * TILE_SIZE)

    if self._texture:
        self._texture = pygame.transform.scale(self._texture, transform_size)

    if self._normal_map:
        self._normal_map = pygame.transform.scale(self._normal_map, transform_size)


  def setTexture(self, texture_path: str, normal_texture_path: str = None) -> None:
    self._texture_path = texture_path
    if(normal_texture_path != None): self._normal_texture_path = normal_texture_path
    
    try:
      self._texture = pygame.image.load(self._texture_path)
    except (pygame.error, FileNotFoundError) as e:
      print(f"Failed to load {self._texture_path}: {e}.")
      self._texture = ERROR_TEXTURE

    if self._normal_texture_path:
      try:
        self._normal_map = pygame.image.load(self._normal_texture_path)
      except (pygame.error, FileNotFoundError) as e:
        print(f"Failed to load normal map: {e}.")
        self._normal_map = None


  def _applyLighting(self, render_pos: np.ndarray[int], lights: list[Light]):
    if self._texture is None:
      self.setTexture(self._texture_path)
      self.setSize(self._size)

    width, height = self._texture.get_size()

    tex_array = pygame.surfarray.array3d(self._texture).astype(np.float32)  # (w,h,3)
    alpha_array = pygame.surfarray.array_alpha(self._texture)  # (w,h)

    if self._normal_map:
      normal_array = pygame.surfarray.array3d(self._normal_map).astype(np.float32)
    else:
      normal_array = np.full((width, height, 3), [128, 128, 255], dtype=np.float32)

    normals = normal_array / 255.0 * 2 - 1
    normals[:, :, 0] *= -1 
    norm_len = np.linalg.norm(normals, axis=2, keepdims=True)
    norm_len[norm_len == 0] = 1
    normals /= norm_len

    xs = np.arange(width) + render_pos[0]
    ys = np.arange(height) + render_pos[1]
    world_x, world_y = np.meshgrid(xs, ys, indexing="ij")
    world_pos = np.stack([world_x, world_y, np.zeros_like(world_x)], axis=2).astype(np.float32)

    total = np.zeros_like(tex_array, dtype=np.float32)

    for light in lights:
      light_pos = np.array(light.position).reshape((1, 1, 3))
      light_dir = light_pos - world_pos
      norm = np.linalg.norm(light_dir, axis=2, keepdims=True)
      norm[norm == 0] = 1
      light_dir /= norm

      intensity = np.clip(np.sum(normals * light_dir, axis=2, keepdims=True), 0, 1)
      total += tex_array * intensity * light.strength * np.array(light.color).reshape((1,1,3))

    total = np.clip(total, 0, 255).astype(np.uint8)

    lit_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.surfarray.blit_array(lit_surface, total)
    pygame.surfarray.pixels_alpha(lit_surface)[:, :] = alpha_array

    self.lit_surface = lit_surface
  

  def getTexture(self, render_pos: np.ndarray[int], lights: list[Light]) -> pygame.Surface:
    if(self.lit_surface == None or not np.array_equal(self._last_pos, render_pos)):
        self._applyLighting(render_pos, lights)

    self._last_pos = render_pos
    return self.lit_surface
