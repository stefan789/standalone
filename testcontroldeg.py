import controldeg as cd
import collections

coils = collections.OrderedDict([
            ("A-X", dict([('Amp', 4),('Freq', 1),('Dur', 10),('Keep', 1)])), 
            ("A-Y", dict([('Amp', 3),('Freq', 5),('Dur', 2),('Keep', 1)])), 
            ("A-Z", dict([('Amp', 3.5),('Freq', 5),('Dur', 6),('Keep', 1)])),       
            ("I-X", dict([('Amp', 9.5),('Freq', 7),('Dur', 8),('Keep', 1)])),
            ("I-Y", dict([('Amp', 8.7),('Freq', 8),('Dur', 7),('Keep', 1)])), 
            ("I-Z", dict([('Amp', 9.1),('Freq', 10),('Dur', 6),('Keep', 1)])), 
            ("All", dict([('Amp', 0),('Freq', 16),('Dur', 5),('Keep', 1)])),
            ("Offset", 0),
            ("Device", "Dev1")])

c = cd.controldega(coils)
c.degauss()
