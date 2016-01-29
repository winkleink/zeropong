import pygame
from gpiozero import MCP3008
from time import sleep
from time import time

threshold = [0,0,0,0,0,0]
detected = 0
multiplier = 1.15
score = 0 
highscore = 0
running = True # Is the program running
ingame = True # Is a game being played
gamelength = 120 # length of a game in seconds

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.get_init

cupsound = "/home/pi/winkleink/zeropong/sound7.ogg"
musicsound = "/home/pi/winkleink/zeropong/organ.wav"
a = pygame.mixer.Sound(cupsound)
a.set_volume(1)
pygame.mixer.music.load(musicsound)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
#a.play()



# window = pygame.display.set_mode((1000,600),pygame.FULLSCREEN)
window = pygame.display.set_mode((1000,700),)
pygame.display.set_caption("Albert\'s Bad Day")
textfont = pygame.font.SysFont("moonspace",100)
# scoretext = textfont.render("Score: " + str(score), 1, (255,255,255))
# window.blit(scoretext, (20,100))
# pygame.draw.rect(window, (255,0,0), (0,0,50,30))
pygame.display.update()


# Get the Threshold for each of the cups (LDRs) 
# Do at the start of each game in case the light has changed

while running == True:
    score = 0
    window.fill((0,0,0))
    scoretext = textfont.render("Score: " + str(score), 1, (255,255,255))
    window.blit(scoretext, (20,100))
    highscoretext = textfont.render("High Score: " + str(highscore), 1, (255,255,255))
    window.blit(highscoretext, (20,300))
    pygame.display.update()

    for x in range(0 ,6):
        with MCP3008(channel=x) as reading:
            threshold[x] = reading.value * multiplier
            print "threshold:" + str(x) +" is " + str(threshold[x])
    # sleep(2)

    starttime = time()
    endtime = starttime + gamelength
    print ("starttime is : " + str(starttime))
    print ("endtime is : " + str(endtime))
    
    ingame = True # set ingame just as the game starts
    while running == True and ingame == True and time() < endtime:    
        pygame.draw.rect(window, (0,0,0), (20,500,500,90))
        timertext = textfont.render("Time: " + str(int(endtime - time())),1,(255,255,255))
        window.blit(timertext, (20,500))
        pygame.display.update()

        # Is Quit done
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                ingame = False

        # Check cups (ldr)
        for x in range(0, 6):
            with MCP3008(channel=x) as reading:
                ldr = reading.value
#               print ("ldr number: " + str(x) + " is " + str(ldr))
#               sleep(0.2)
            
            
            if ldr > threshold[x] and ldr < 0.9:
                a.play()
                score =score + (100 * (x+1))
                if score > highscore:
                    highscore = score
                window.fill((255,0,0))
                scoretext = textfont.render("Score: " + str(score), 1, (255,255,255))
                window.blit(scoretext, (20,100))
                highscoretext = textfont.render("High Score: " + str(highscore), 1, (255,255,255))
                window.blit(highscoretext, (20,300))
                pygame.display.update()

                detected = 1
                print ("ldr number: " + str(x) + " is " + str(ldr))
                while ldr >threshold [x] and ldr < 0.9:
                    with MCP3008(channel=x) as reading:
                        ldr = reading.value
                        print ("ldr number: " + str(x) + " has been activated - value is " + str(ldr))
                if detected == 1:
                    sleep(2)
                    print ("\nReady\n")
                    window.fill((0,0,0))
                    scoretext = textfont.render("Score: " + str(score), 1, (255,255,255))
                    window.blit(scoretext, (20,100))
                    highscoretext = textfont.render("High Score: " + str(highscore), 1, (255,255,255))
                    window.blit(highscoretext, (20,300))
                    pygame.display.update()
                    detected = 0
                    # sleep(1)
    
    ingame = False
    print ("Game Over")
    window.fill((0,0,0))
    if score == highscore:
        scoretext = textfont.render("Score: " + str(score), 1, (255,0,0))
    else:
        scoretext = textfont.render("Score: " + str(score), 1, (255,255,255))
    window.blit(scoretext, (20,100))
    highscoretext = textfont.render("High Score: " + str(highscore), 1, (255,255,255))
    window.blit(highscoretext, (20,300))
    if score == highscore:
        newhightext = textfont.render("NEW HIGH SCORE!!!", 1, (255,0,0))
    window.blit(newhightext, (20,500))
    pressakey = textfont.render("Press Enter to Play Again",1,(0,255,0))
    window.blit(pressakey, (100,20))
    pygame.display.update()
    
    while ingame == False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ingame = True
                    
#    sleep(2)
