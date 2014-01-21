import digiinportthread as di

d = di.DigiInPortThread("Dev1", 1)
dat = d.readi()

print "Test print: " + str(dat)

d = di.DigiInPortThread("Dev1", 0)
dat = d.readi()

print "Test print: " + str(dat)

d = di.DigiInPortThread("Dev1", 2)
dat = d.readi()

print "Test print: " + str(dat)
