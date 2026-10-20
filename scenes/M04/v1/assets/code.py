def mix(voice, bgm):
    level = -18
    if voice.active:
        level -= 8
    return bgm.gain(level) + voice
