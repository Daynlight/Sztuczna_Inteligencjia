import pygame
import numpy as np
from PIL import Image

from Classes.Core.Renderer.Light import Light
from conf import TILE_SIZE, DYNAMIC_LIGHTS, ERROR_TEXTURE, DEBUG





class Texture:
  def __init__(self, texture_path: str, normal_texture_path: str = "", size: np.ndarray[int] = np.array([1, 1], dtype=int)):
    self._texture_path: str = texture_path
    self._normal_texture_path: str = normal_texture_path
    self._size: np.ndarray[int] = size
    self._texture: pygame.Surface = None
    self._normal_map: pygame.Surface = None


  def precomputeLight(self, render_pos: np.ndarray[int], light: np.ndarray[Light]) -> None:
    self.setTexture(self._texture_path, self._normal_texture_path)
    self.setSize(self._size)


  def setSize(self, size: np.ndarray[int]) -> None:
    self._size = size
    transform_size = (self._size[0] * TILE_SIZE, self._size[1] * TILE_SIZE)

    if self._texture:
      self._texture = pygame.transform.scale(self._texture, transform_size)

    if self._normal_map:
      self._normal_map = pygame.transform.scale(self._normal_map, transform_size)


  def pil_to_surface(self, pil_img):
    mode = pil_img.mode
    size = pil_img.size
    data = pil_img.tobytes()
    return pygame.image.fromstring(data, size, mode)


  def setTexture(self, texture_path: str, normal_texture_path: str = None) -> None:
    self._texture_path = texture_path
    self._normal_texture_path = normal_texture_path

    try:
      self._texture = self.pil_to_surface(Image.open(self._texture_path).convert("RGBA"))
    except (pygame.error, FileNotFoundError) as e:
      if(DEBUG): print(f"Failed to load {self._texture_path}: {e}.")
      self._texture = ERROR_TEXTURE

    if self._normal_texture_path and DYNAMIC_LIGHTS == True:
      try:
        self._normal_map = self.pil_to_surface(Image.open(self._normal_texture_path).convert("RGBA"))
      except (pygame.error, FileNotFoundError) as e:
        if(DEBUG): print(f"Failed to load normal map: {e}.")
        self._normal_map = None


  def _applyLighting(self, render_pos: np.ndarray[int], lights: list[Light]) -> None:
    if self._texture is None:
      self.setTexture(self._texture_path)
      self.setSize(self._size)

    if(DYNAMIC_LIGHTS == False): return self._texture

    width, height = self._texture.get_size()

    tex_array = pygame.surfarray.array3d(self._texture).astype(np.float32)
    alpha_array = pygame.surfarray.array_alpha(self._texture)

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

    light_positions = np.array([light.position for light in lights], dtype=np.float32)
    light_colors = np.array([light.color for light in lights], dtype=np.float32)
    light_strengths = np.array([light.strength for light in lights], dtype=np.float32)

    light_dir = light_positions[:, None, None, :] - world_pos[None, :, :, :]
    norm = np.linalg.norm(light_dir, axis=3, keepdims=True)
    norm[norm == 0] = 1
    light_dir /= norm

    intensity = np.clip(np.sum(normals[None, :, :, :] * light_dir, axis=3, keepdims=True), 0, 1)

    total = np.sum(tex_array[None, :, :, :] * intensity * light_strengths[:, None, None, None] * light_colors[:, None, None, :], axis=0)
    total = np.clip(total, 0, 255).astype(np.uint8)

    lit_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.surfarray.blit_array(lit_surface, total)
    pygame.surfarray.pixels_alpha(lit_surface)[:, :] = alpha_array

    return lit_surface


  def getTexture(self, render_pos: np.ndarray[int], lights: list[Light]) -> pygame.Surface:
    return self._texture
  

  def getLitTexture(self, render_pos: np.ndarray[int], lights: list[Light]) -> pygame.Surface:
    return self._applyLighting(render_pos, lights)
