from app.core.capture import grab_region

# Coordenadas ficticias apenas para testar o script de captura
# Futuramente será criado um script de overlay com pyside6

bbox = (100,100,600,400)

img = grab_region(bbox)
img.show()