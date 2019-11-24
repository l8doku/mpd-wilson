from math import sqrt
import argparse
import musicpd

def wilson_lower_bound(likes, dislikes, z=1.44):
    total = likes + dislikes
    if total < 1:
        return 0
    likes_rel = likes / total
    denominator = 1 + z**2/total
    centre_adjusted_probability = likes_rel + z*z / (2*total)

    adjusted_standard_deviation = sqrt((likes_rel*(1 - likes_rel) + z*z / (4*total)) / total)

    lower_bound = (centre_adjusted_probability - z*adjusted_standard_deviation) / denominator
    # upper_bound = (centre_adjusted_probability + z*adjusted_standard_deviation) / denominator
    return lower_bound

def run(args):
    cli = musicpd.MPDClient()
    cli.connect()

    uri = cli.currentsong().get('file')

    try:
        likes = cli.sticker_get('song', uri, 'likes')
        likes_offset = len('likes=')
        likes = int(likes[likes_offset:])
    except musicpd.CommandError:
        likes = 0

    try:
        dislikes = cli.sticker_get('song', uri, 'dislikes')
        dislikes_offset = len('dislikes=')
        dislikes = int(dislikes[dislikes_offset:])
    except musicpd.CommandError:
        dislikes = 0

    if args.verbose:
        try:
            wrating = cli.sticker_get('song', uri, 'wrating')
            wrating_offset = len('wrating=')
            wrating = wrating[wrating_offset:]
        except musicpd.CommandError:
            print("No rating yet")
            wrating = 0
        print('Likes before update    =', likes)
        print('Dislikes before update =', dislikes)
        print('Rating before update   =', wrating)


    if args.like:
        likes += 1
    elif args.dislike:
        dislikes += 1
    elif args.unlike:
        likes = max(0, likes - 1)
    elif args.undislike:
        dislikes = max(0, dislikes - 1)

    wrating = wilson_lower_bound(likes, dislikes)


    likes = str(likes)
    dislikes = str(dislikes)
    wrating = '{0:.10f}'.format(wrating)

    cli.sticker_set('song', uri, 'likes', likes)
    cli.sticker_set('song', uri, 'dislikes', dislikes)
    cli.sticker_set('song', uri, 'wrating', wrating)


    if args.notify:
        import notify2
        notify2.init("Rating notifier")
        notify_text = ""
        if args.like:
            notify_text = "Liked!\n"
        elif args.dislike:
            notify_text = "Disliked!\n"
        elif args.unlike:
            notify_text = "Unliked!\n"
        elif args.undislike:
            notify_text = "Undisiked!\n"

        notify_text += "L: " + str(likes) + "\n"
        notify_text += "D: " + str(dislikes) + "\n"
        notify_text += "R: " + str(wrating) + "\n"
        n = notify2.Notification("Rating",
                            notify_text,
                            "notification-message-im"   # Icon name
                            )
        n.set_timeout(1000)

        n.show()

    if args.verbose:
        print('Likes after update    =', likes)
        print('Dislikes after update =', dislikes)
        print('Rating after update   =', wrating)


    cli.disconnect()


def get_args():
    parser = argparse.ArgumentParser(description='Rate the currently playing song',)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--like", action="store_true")
    group.add_argument("-ul", "--unlike", action="store_true")
    group.add_argument("-d", "--dislike", action="store_true")
    group.add_argument("-ud", "--undislike", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-n", "--notify", action="store_true")

    args = parser.parse_args()
    return args

def main():
    args = get_args()
    run(args)

# Script starts here
if __name__ == '__main__':
    main()

