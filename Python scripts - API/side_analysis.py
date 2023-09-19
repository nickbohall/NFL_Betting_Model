from matplotlib import pyplot as plt
import matplotlib.ticker as mplt
def plot_epa(data, team):

    # Let's do some plotting to see what the data looks like
    tm = data.loc[data['team'] == team, :].assign(
        season_week = lambda x: 'w' + x.week.astype(str) + ' (' + x.season.astype(str) + ')').set_index('season_week')

    fig, ax = plt.subplots()

    loc = mplt.MultipleLocator(base=16) # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)
    ax.tick_params(axis='x', rotation=75) #rotate the x-axis labels a bit

    ax.plot(tm['epa_shifted_passing_offense'], lw=1, alpha=0.5)
    ax.plot(tm['ewma_dynamic_window_passing_offense'], lw=2)
    ax.plot(tm['ewma_passing_offense'], lw=2);
    plt.axhline(y=0, color='red', lw=1.5, alpha=0.5)

    ax.legend(['Passing EPA', 'EWMA on EPA with dynamic window', 'Static 10 EWMA on EPA'])
    ax.set_title('GB Passing EPA per play')
    plt.show()