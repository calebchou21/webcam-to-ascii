import cv2
import curses

# Density string
DENSITY = "@#W$9876543210?!abc;:+=-,._        "
#DENSITY = r"$@8W*ohkbdqwmO0LCYXzcunrft/\|()1{}[]?_>ilI:,'`'            "


def intensity_to_ascii(intensity):
    scaled_intensity = int((intensity / 255) * (len(DENSITY) - 1))
    return DENSITY[scaled_intensity]

def initialize_curses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr

def clear_screen(stdscr):
    stdscr.clear()

def cleanup_curses(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def main(stdscr):
    while True:
        rows, cols = stdscr.getmaxyx()
        ret, frame = vid.read()

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        new_cols = int(cols - 1)
        new_rows = int(rows - 1)
        dim = (new_cols, new_rows)
        frame = cv2.resize(gray_frame, dim, interpolation=cv2.INTER_AREA)

        ascii_art = ""
        for row in frame:
            for intensity in row:
                ascii_art += intensity_to_ascii(intensity)
            ascii_art += "\n"

        clear_screen(stdscr)
        stdscr.addstr(0, 0, ascii_art)
        stdscr.refresh()

if __name__ == "__main__":
    try:
        vid = cv2.VideoCapture(0)
        stdscr = initialize_curses()
        curses.wrapper(main)
    finally:
        cleanup_curses(stdscr)
        vid.release()
        cv2.destroyAllWindows()
