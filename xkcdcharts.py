import io
from typing import Sequence

from errbot import BotPlugin, arg_botcmd
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # needs to be done after matplotlib.use
plt.xkcd()
from threading import Lock
mpl_lock = Lock()


def synchronized(lock):
    def wrap(f):
        def wrapped(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return wrapped
    return wrap


def parse_tuple(t: str) -> (int, int):
    x, y = t.split(',')
    return int(x), int(y)


class Charts(BotPlugin):

    def save_chart(self, plt):
        with io.BytesIO() as img:
            plt.savefig(img, format='png')
            img.seek(0, 0)
            req = requests.post('http://uploads.im/api',
                                files={'upload': ('chart.png', img)})
            res = req.json()
            url = res['data']['thumb_url'].replace('.im/t/', '.im/d/')
            return url

    @synchronized(mpl_lock)
    def _xy(self, coords: Sequence[str]=None, note=None, xlim=None, ylim=None, xlabel=None, ylabel=None):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        plt.xticks([])
        plt.yticks([])
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        ax.set_xlim(xlim or [0, 120])
        ax.set_ylim(ylim or [0, 120])
        if coords:
            xs, ys = zip(*(parse_tuple(coord) for coord in coords))
            plt.plot(xs, ys, 'r')
        if note:
            note_msg, xy, xy_txt = note
            plt.annotate(note_msg, xy=parse_tuple(xy), arrowprops=dict(arrowstyle='->'), xytext=parse_tuple(xy_txt))
        return self.save_chart(plt)

    @arg_botcmd('coords', metavar='coords', type=str, nargs='*', help='coordinates to plot a line in x1,y1 x2,y2'
                                                                      'separated by space')
    @arg_botcmd('--note', dest='note', type=str, nargs=3, help='a note with first the pointed point on the chart and'
                                                               'then the spot for the text like:'
                                                               '"The balmer peak" 70,100 15,50')
    @arg_botcmd('--xlim', dest='xlim', type=str, nargs=1, help='min and max for x axis like -10,10'
                                                               'default is 0,120')
    @arg_botcmd('--ylim', dest='ylim', type=str, nargs=1, help='min and max for y axis like -10,10'
                                                               'default is 0,120')
    @arg_botcmd('--xlabel', dest='xlabel', type=str, nargs=1, help='label for the x axis')
    @arg_botcmd('--ylabel', dest='ylabel', type=str, nargs=1, help='label for the y axis')
    def xy(self, _, coords=None, note=None, xlim=None, ylim=None, xlabel=None, ylabel=None):
        return self._xy(coords=coords, note=note, xlim=xlim, ylim=ylim, xlabel=xlabel, ylabel=ylabel)

    @arg_botcmd('note', type=str, nargs=1, help='Why it is going down ?')
    @arg_botcmd('--xlabel', dest='xlabel', type=str, nargs=1, help='label for the x axis')
    @arg_botcmd('--ylabel', dest='ylabel', type=str, nargs=1, help='label for the y axis')
    def downchart(self, _, note=None, xlabel=None, ylabel=None):
        """
        Just a canned case of xy with those parameters:
           !downchart Crosstalk [--xlabel time] [--ylabel money]
           !xy 0,100 70,100 100,0 --note [your message] 70,100 15,50 [--xlabel ...] [--ylabel ...]
        """
        return self._xy(note=(note[0], '70,100', '15,50'),
                        coords=('0,100', '70,100', '100,0'),
                        xlabel=xlabel[0] if xlabel else None,
                        ylabel=ylabel[0] if ylabel else None)

    @arg_botcmd('note', type=str, nargs=1, help='Why it is going down ?')
    @arg_botcmd('--xlabel', dest='xlabel', type=str, nargs=1, help='label for the x axis')
    @arg_botcmd('--ylabel', dest='ylabel', type=str, nargs=1, help='label for the y axis')
    def upchart(self, _, note=None, xlabel=None, ylabel=None):
        """
        Just a canned case of xy with those parameters:
           !upchart "your message" Message [--xlabel time] [--ylabel money]
           !xy 0,100 70,100 100,0 --note [your message] 70,100 15,50
        """
        return self._xy(note=(note[0], '70,10', '15,50'),
                        coords=('0,10', '70,10', '100,100'),
                        xlabel=xlabel[0] if xlabel else None,
                        ylabel=ylabel[0] if ylabel else None)
