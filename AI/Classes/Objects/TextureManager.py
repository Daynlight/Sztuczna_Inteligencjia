import os
import pygame

from Classes.Core.Renderer.Texture import Texture









PATH_TO_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "Assets")










# Tile Texture
TILE_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Grid", "Tile", "Tile.png"), size=[2,2])

# Wall Texture
WALL1_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Wall", "Wall1.png"),
																			normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Wall", "Wall1_Normals.png"),
                                      size=[2, 4])

WALL1_ROTATED_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Wall", "Wall1_rotated.png"),
																			normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Wall", "Wall1_Normals_rotated.png"),
                                      size=[2, 4])

WALL2_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Wall", "Wall2.png"), 
                                      normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Wall", "Wall2_Normals.png"),
                                      size=[2, 4])

WALL2_ROTATED_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Wall", "Wall2_rotated.png"), 
                                      normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Wall", "Wall2_Normals_rotated.png"),
                                      size=[2, 4])

WALL1_2_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Wall", "Wall1-2.png"), 
                                      normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Wall", "Wall1-2_Normals.png"),
                                      size=[2, 4])

WALL1_2_ROTATED_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Wall", "Wall1-2_rotated.png"), 
                                      normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Wall", "Wall1-2_Normals_rotated.png"),
                                      size=[2, 4])

# Client
CLIENT_TEXTURE = Texture(os.path.join(PATH_TO_ASSETS, "Other", "client.png"))

# Chairs
CHAIR1_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Chair", "Chair1.png"),
																		 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Chair", "Chair1_Normals.png"),
																		 size=[2, 2])

CHAIR2_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Chair", "Chair2.png"),
																		 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Chair", "Chair2_Normals.png"),
																		 size=[2, 2])

CHAIR3_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Chair", "Chair3.png"),
																		 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Chair", "Chair3_Normals.png"),
																		 size=[2, 2])

CHAIR4_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Chair", "Chair4.png"),
																		 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Chair", "Chair4_Normals.png"),
																		 size=[2, 2])

# Couch

COUCH2_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Couch", "Couch2.png"),
																		 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Couch", "Couch2_Normals.png"),
																		 size=[2, 4])

COUCH3_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Couch", "Couch3.png"),
																		 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Couch", "Couch3_Normals.png"),
																		 size=[2, 4])

COUCH_MIDDLE_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Couch", "Couch_Middle.png"),
																		 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Couch", "Couch_Middle_Normals.png"),
																		 size=[2, 4])


# Table
TABLE_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Table", "Table.png"), 
									 	 								 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Table", "Table_Normals.png"),
																		 size=[2, 2])
                                     
# Counter
COUNTER_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Counter", "Counter.png"), 
									   								 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Counter", "Counter_Normals.png"),
																		 size=[2, 2])

# Cook
COOK1_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Being", "Cook", "Idle", "Cook_1.png"), 
									   								 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Being", "Cook", "Idle", "Cook_1_Normals.png"),
																		 size=[1, 2]) 

# Waiter
WAITER_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Being", "Waiter", "Kerfus.png"), 
														         normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Being", "Waiter", "Kerfus_Normals.png"),
																		 size=[1, 2]) 

# Flower
FLOWER_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Flower", "Flower.png"), 
									   								 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Flower", "Flower_Normals.png"),
																		 size=[2, 2]) 

# Sink
SINK_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Sink", "Sink.png"), 
									   								 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Sink", "Sink_Normals.png"),
																		 size=[2, 2])
 
# Order List
ORDER_LIST_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Order_List", "Order_List.png"), 
									   								 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Order_List", "Order_List_Normals.png"),
																		 size=[2, 2])

# Fridge
FRIDGE_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Fridge", "Fridge.png"), 
									   								 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Fridge", "Fridge_Normals.png"),
																		 size=[2, 4])
 
# Stove
STOVE_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Stove", "Stove.png"), 
									   								 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Stove", "Stove_Normals.png"),
																		 size=[2, 2])

# Dishwasher

DISHWASHER_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Dishwasher", "Dishwasher.png"), 
									   								 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Dishwasher", "Dishwasher_Normals.png"),
																		 size=[2, 2])
 
# Painting

PAINTING_TEXTURE = Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Paintings", "Painting.png"), 
									   								 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Paintings", "Painting_Normals.png"),
																		 size=[2, 4])

# Carpet

CARPET_TEXTURE= Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Carpet", "Carpet.png"),
																		 size=[2, 1])