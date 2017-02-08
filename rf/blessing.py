from blessings import Terminal
import time

escalation_level = 0
escalations = {
	0: (7,2,"* * * *    O K    * * * *","Stufe 0: Es scheint alles in Ordnung."),
	1: (0,7,"* * * W A R N U N G * * *","Stufe 1: Reaktion vom Nutzer erforderlich..."),
	2: (7,3,"* * * W A R N U N G * * *","Stufe 2: Unterstuetzung bei Ansprechpartner angefordert."),
	3: (7,1,"* * * * A L A R M * * * *","Stufe 3: Alarm-Zustand. Sofortige Unterstuetzung erforderlich!"),
}

# #############################################################

term = Terminal()

def term_init():
	print term.enter_fullscreen()
	print term.clear()

def term_exit():
	print term.exit_fullscreen()
	print term.move(0,term.height-1)

def term_escalation(fcode=7, bcode=0, title="", message="", delimiter="*"):
	term.clear()

	# background
	for x in xrange(20):
		with term.location(0,x):
			print term.on_color(bcode) + ' ' * int(term.width)

	# title
	title_pos=term.width/2-len(title)/2
	with term.location(title_pos,7):
		print term.on_color(bcode) + term.color(fcode) + term.bold + (delimiter * len(title))
	with term.location(title_pos,8):
		print term.on_color(bcode) + term.color(fcode) + term.bold + title
	with term.location(title_pos,9):
		print term.on_color(bcode) + term.color(fcode) + term.bold + (delimiter * len(title))
	# message
	with term.location(term.width/2-len(message)/2,12):
		print term.on_color(bcode) + term.color(fcode) + term.bold + message



term_init()
(esc_fcolor, esc_bcolor, esc_title, esc_message) = escalations.get(escalation_level)
term_escalation(esc_fcolor, esc_bcolor, esc_title, esc_message)
term_exit()
time.sleep(10)
