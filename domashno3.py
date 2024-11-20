class Tone:
    _NUMBER_OF_TONES = 12

    tones = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
 
    def __init__(self, name):
        if name in self.tones:
            self.name = name
 
    def __str__(self):
        return self.name
 
    def __add__(self, other):
        if isinstance(other, Tone):
            return Chord(self, other)
        elif isinstance(other, Interval):
            ind = self.tones.index(self.name)
            new_ind = (ind+other.number_of_semitones) % self._NUMBER_OF_TONES
            return Tone(self.tones[new_ind])
 
    def __sub__(self, other):
        if isinstance(other, Tone):
            number_of_semitones = (Tone.tones.index(self.name)-Tone.tones.index(other.name)) % self._NUMBER_OF_TONES
            return Interval(number_of_semitones)
        elif isinstance(other, Interval):
            ind = self.tones.index(self.name)
            new_ind = (ind - other.number_of_semitones) % self._NUMBER_OF_TONES
            return Tone(self.tones[new_ind])
        

class Interval:
    _NUMBER_OF_SEMITONES = 12
    intervals = {
        0: "unison", 1: "minor 2nd", 2: "major 2nd", 3: "minor 3rd",
        4: "major 3rd", 5: "perfect 4th", 6: "diminished 5th",
        7: "perfect 5th", 8: "minor 6th", 9: "major 6th",
        10: "minor 7th", 11: "major 7th"
        }
 
    def __init__(self, number_of_semitones):
        self.number_of_semitones = number_of_semitones % self._NUMBER_OF_SEMITONES
 
    def __str__(self):
        return self.intervals[self.number_of_semitones]
 
    def __add__(self, other):
        if isinstance(other, Tone):
            raise TypeError("Invalid operation")
        elif isinstance(other, Interval):
            new_num_of_semitones = self.number_of_semitones + other.number_of_semitones
            return Interval(new_num_of_semitones)
 
    def __sub__(self, other):
        if isinstance(other, Tone):
            raise TypeError("Invalid operation")

    #used in the transpose function in order to add a negative interval to a tone 
    def __neg__(self): 
        """Convert an interval to the negative value."""
        return Interval(-self.number_of_semitones)
    

class Chord:
    _NUMBER_OF_SEMITONES = 12
    _MIN_UNIQUE_TONES_IN_CHORD = 2
    _NUMBER_OF_SEMITONES_IN_MINOR = 3
    _NUMBER_OF_SEMITONES_IN_MAJOR = 4
    
    def __init__(self, main_tone, *other_tones):
        unique_tone_names = {main_tone.name}
        unique_tones = [main_tone]
 
        for tone in other_tones:
            if tone.name not in unique_tone_names:
                unique_tone_names.add(tone.name)
                unique_tones.append(tone)
 
        if len(unique_tone_names) < self._MIN_UNIQUE_TONES_IN_CHORD:
            raise TypeError("Cannot have a chord made of only 1 unique tone")
 
        main_tone_ind = Tone.tones.index(main_tone.name)
        self.main_tone_ind = main_tone_ind #so I can use it in _get_distance_from_main_tone
        tones_left = list()

        for tone in unique_tones:
            if tone != main_tone:
                tones_left.append(tone)

        tones_left.sort(key = self._get_distance_from_main_tone)

        self.tones = [main_tone]
        for tone in tones_left:
            self.tones.append(tone)
            
    def _get_tones_diff(self, tone, main_tone_ind):
        """Return the count of semitones between a tone and the main_tone_ind."""
        return (Tone.tones.index(tone.name) - main_tone_ind) % self._NUMBER_OF_SEMITONES
    
    def _get_distance_from_main_tone(self, tone):
        """Calculate the difference between the current tone and the main tone of the chord in semitones."""
        return self._get_tones_diff(tone, self.main_tone_ind)
         
    def _get_tone_ind(self, tone_name):
        """Return the index of a tone."""
        return Tone.tones.index(tone_name)
 
    def __str__(self):
        return f"{'-'.join(str(tone) for tone in self.tones)}"
 
    def _is_interval(self, semitones_count):
        main_tone = self.tones[0]
        main_tone_ind = self._get_tone_ind(main_tone.name)
        tones_count = len(self.tones)

        for t in range(1, tones_count):
            tone = self.tones[t]
            tone_ind = self._get_tone_ind(tone.name)
            if((tone_ind - main_tone_ind) % self._NUMBER_OF_SEMITONES == semitones_count):
                return True
 
        return False
 
    def is_minor(self):
        return self._is_interval(self._NUMBER_OF_SEMITONES_IN_MINOR)
 
    def is_major(self):
        return self._is_interval(self._NUMBER_OF_SEMITONES_IN_MAJOR)
 
    def is_power_chord(self):
        if not self.is_minor() and not self.is_major():
            return True
        
        return False
    
    def _create_chord(self, new_tones):
        """Create a new chord."""
        new_main_tone = new_tones[0]
        new_other_tones = new_tones[1:]

        return Chord(new_main_tone, *new_other_tones)
    
    def __add__(self, other):
        tones_in_new_chord = list(self.tones)

        if isinstance(other, Tone):
            if other not in tones_in_new_chord:
                tones_in_new_chord.append(other)
            return self._create_chord(tones_in_new_chord)
        elif isinstance(other, Chord):
            for tone in other.tones:
                if tone not in tones_in_new_chord:
                    tones_in_new_chord.append(tone)

            return self._create_chord(tones_in_new_chord)
        
    def __sub__(self, other):
        if isinstance(other, Tone):
            if other.name not in (tone.name for tone in self.tones):
                raise TypeError(f"Cannot remove tone {other} from chord {self}")

            tones_in_new_chord = list()

            for tone in self.tones:
                if tone.name != other.name:
                    tones_in_new_chord.append(tone)

            if len(tones_in_new_chord) < self._MIN_UNIQUE_TONES_IN_CHORD:
                raise TypeError("Cannot have a chord made of only 1 unique tone")

            return self._create_chord(tones_in_new_chord)
    
    def transposed(self, interval):
        if isinstance(interval, Interval):
            tones_in_new_chord = list()
            for tone in self.tones:
                new_tone = tone + interval
                tones_in_new_chord.append(new_tone)

            return self._create_chord(tones_in_new_chord)