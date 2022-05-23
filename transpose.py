import argparse

enharmonic_flats = {
  'Cb': 'B',
  'Db': 'C#',
  'Eb': 'D#',
  'Fb': 'E',
  'Gb': 'F#',
  'Ab': 'G#',
  'Bb': 'A#'
}

enharmonic_sharps = {
  'C#': 'Db',
  'D#': 'Eb',
  'E#': 'F',
  'F#': 'Gb',
  'G#': 'Ab',
  'A#': 'Bb',
  'B#': 'C'
}

scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

all_tones = set(scale)
all_tones.update(enharmonic_flats.keys())

def _transpose_single(note: str, tones: int, accidental: str) -> str:
    orig_note = note

    if len(note) == 1:
        note = note[0]
        index = 1
    elif note[1] == '#' or note[1] == 'b':
        note = note[:2]
        index = 2
    else:
        note = note[0]
        index = 1

    swapped = False
    if note in enharmonic_flats:
        note = enharmonic_flats[note]
        swapped = True
    note = scale[(scale.index(note) + tones) % len(scale)]

    if accidental:
        if accidental == '#' and note in enharmonic_flats:
            note = enharmonic_flats[note]
        elif accidental == 'b' and note in enharmonic_sharps:
            note = enharmonic_sharps[note]
    else:
        if swapped and note in enharmonic_sharps:
            note = enharmonic_sharps[note]
    
        if tones < 0 and note in enharmonic_sharps:
            note = enharmonic_sharps[note]
        elif tones > 0 and note in enharmonic_flats:
            note = enharmonic_flats[note]

    return note + orig_note[index:]

def transpose_chord(chord: str, tones: int, accidental: str) -> str:
    if '/' in chord:
        p1, p2 = chord.split('/')
        return _transpose_single(p1, tones, accidental) \
            + '/' \
            + _transpose_single(p2, tones, accidental)
    else:
        return _transpose_single(chord, tones, accidental) 
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transpose chord sheet. +/- some semitones')
    parser.add_argument('input', metavar='I', type=str,
        help='input file path')
    parser.add_argument('output', metavar='O', type=str,
        help='output file path')
    parser.add_argument('-i', '--intervals', type=int,
        help='number of semitones up or down (+/-) to transpose')
    parser.add_argument('-a', '--accidental', type=str,
        help='b or # to prefer one accidental enharmonic over the other')
    args = parser.parse_args()
    
    if not args.intervals:
        print("Transpose Intervals Expected")
        exit()
    if args.accidental and args.accidental != '#' and args.accidental != 'b':
        print("accidental must either be 'b' or '#'")
        exit()

    with open(args.input, 'r') as f:
        with open(args.output, 'w+') as w:
            for line in f:
                tokens = line.split() # reverse for
                tokens.reverse()

                if tokens and all(t[0] in all_tones for t in tokens):
                    output_line = ""
                    i = 0
                    while i < len(line):
                        if line[i].isspace():
                            output_line += line[i]
                            i+=1
                        else:
                            chord = tokens.pop()
                            output_line += transpose_chord(
                                    chord, 
                                    args.intervals, 
                                    args.accidental)
                            i += len(chord)
                else:
                    output_line = line
                w.write(output_line) 
