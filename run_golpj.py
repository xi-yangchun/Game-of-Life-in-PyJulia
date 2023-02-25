import numpy as np
import pygame
from pygame.locals import *
import sys
import cv2

def printstate(state,narr):
    print('state,narr=')
    for i in range(state.shape[0]):
        s=''
        for j in range(state.shape[1]):
            s=s+'{},{} '.format(state[i,j],narr[i,j])
        print(s)
    print('\n')

def main():
    from julia import Main
    Main.include("golutil.jl")

    h,w=70,70
    state=Main.make_rand_life(h,w)
    narr=Main.make_zero_arr(h,w)
    lifedic={"state":state,"narr":narr}

    s=4
    lifetv=pygame.Surface((h,w))
    color=[150,200,250]

    pygame.init()
    screen = pygame.display.set_mode((w*s, h*s))
    clock = pygame.time.Clock() #クロックの設定。異なるPCで異なる速さの動作になることを防ぐ
    pygame.display.set_caption("GOL IN PYJULIA") #タイトルバーに表示する文字

    while(1):
        clock.tick(300)
        screen.fill((0,0,0))
        state=lifedic['state']

        tvarr0=state.astype('uint8')
        tvarr2=pygame.surfarray.pixels3d(lifetv)
        tvarr2[:,:,0]=tvarr0*color[0]
        tvarr2[:,:,1]=tvarr0*color[1]
        tvarr2[:,:,2]=tvarr0*color[2]
        del tvarr2
        screen.blit(pygame.transform.scale(lifetv,(w*s,h*s)),
                    dest=(0,0))
        pygame.display.update()
        lifedic=Main.step(lifedic["state"],
                            lifedic["narr"],
                            h,w)
        #printstate(lifedic["state_memo"],lifedic["narr_memo"])
        #printstate(state,lifedic["narr"])

        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                pygame.quit()       # Pygameの終了(画面閉じられる)
                sys.exit()

if __name__ == '__main__':
    while (1):
        # イベント処理
        main()