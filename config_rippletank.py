
# config_rippletank.py : default configuration file for mix machine

NG = 0							# number of generations

TICKS = 10						# clock ticks	

MAXTIME = 100					# tempo massimo di esecuzione in sec

XRES,YRES,RES = 480,480,4		# screen resolution and dot dimension

DIM = (XRES//RES,YRES//RES)		# dimensione delle matrici di calcolo

DECAY = .00005					# wave decay time
SLIT_X = 150					# posizione orrizontale della slit
SLIT_APERTURE 	= 2				# slit 1/2 aperture
SLIT_TICK 		= 1				# slit tickness
Q = 1							# numero di stati dell'automa

INTENSITY = 250					# luminosita'...che poi decade con l'espandersi dell'onda, quindi va messa un po' alta..