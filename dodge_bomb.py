import time
import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELAT = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル、（横、縦）
    画面内ならTrue、画面外ならFlase
    """
    yoko, tate = True, True  # 横、縦方向用の変数
    #横方向判定
    if rct.left < 0 or WIDTH < rct.right:  # 画面外だったら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 画面外だったら
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    # GameOver用四角イメージ作成
    over_img = pg.Surface((WIDTH, HEIGHT))
    over_img.set_alpha(150)
    # over_imgに黒い四角形を描画 
    pg.draw.rect(over_img, (0,0,0), pg.Rect(0,0,WIDTH,HEIGHT))
    over_rct = over_img.get_rect()
    over_rct.center = WIDTH/2, HEIGHT/2
    screen.blit(over_img,over_rct)
    #文字列を作成
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = (WIDTH/2,HEIGHT/2)
    screen.blit(txt, txt_rct)
    #こうかとん画像を作成＆表示
    kksad_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kksad_rct = kksad_img.get_rect()  # こうかとん一人目
    kksad_rct.center = 350, 325
    screen.blit(kksad_img,kksad_rct)  # こうかとん二人目
    kksad_rct.center = 750, 325
    screen.blit(kksad_img,kksad_rct)
    pg.display.update()
    time.sleep(5)




def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    #こうかとん初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    #爆弾初期化
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = kk_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    vx = +5
    vy = +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        # こうかとんRectと爆弾Rectが衝突したら
        if kk_rct.colliderect(bb_rct):
            gameover(screen)  # GameOver処理を行う
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELAT.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  #左右方向
                sum_mv[1] += mv[1]  #上下方向

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # 画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 画面内に戻す
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 左右どちらかにはみ出ていたら
            vx *= -1
        if not tate:  # 上下どちらかにはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾の描画
        pg.display.update()
        tmr += 1
        clock.tick(50)




if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
