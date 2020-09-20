
from pygame.image import load
import pygame.font as pff

pff.init()
SYSFONT = 'playbill' # 'calibri' or 'freesansbold.ttf' may be used
#do NOT use None

def T(cw,txt,x,y,r=0,g=0,b=0,aliasing=1,size=20,center=True):
	"""allows the display of text on screen with or without centering
	the text will be displayed in the window 'cw'
	"""
	font = pff.SysFont( SYSFONT, size)
	text = font.render(txt, aliasing, (r, g, b))
	if center:
		textpos = text.get_rect(centery=y,centerx=x)
	else:
		textpos = (x,y)
	cw.blit(text, textpos)
	return x,x+text.get_width(),y,y+text.get_height()

def textinabox(j,win,txt,fh,c1,c2,c3,size=30):
	""" used to display text in the left box """
	j += 1
	a1,a2,a3,a4 = T(win,txt,24,fh+30+(size-2)*j,c1,c2,c3,center=False,size=30)
	return j,a1,a2,a3,a4

def textimg(txt,r=4,g=5,b=5,aliasing=1,size=20):
	font = pff.SysFont( SYSFONT, size)
	text = font.render(txt, aliasing, (r, g, b))
	return text