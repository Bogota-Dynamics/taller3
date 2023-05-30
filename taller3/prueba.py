import pygame

pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No se detectaron dispositivos de joystick.")
    pygame.quit()
    exit()
else:
    print("Hay" + str(joystick_count))

print(joystick.get_numbuttons())


while True:

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit()
            quit()
    print(joystick.get_hat(0))
