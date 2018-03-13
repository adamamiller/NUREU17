#schema: https://www.lsst.org/scientists/simulations/opsim/summary-table-column-descriptions-v335
#http://ops2.lsst.org/docs/current/architecture.html

#we need to take an input RA, DEC and find the fieldid that it corresponds to in the "Field" table
#then use fieldid to find the relevant "ObsHistory"

import sqlite3
import numpy as np

from astropy.coordinates import SkyCoord, match_coordinates_sky
from astropy import units


def getFieldID(db, inRA, inDec, deglim = 3.5/2.):
	#field-of-view == 3.5-degree diameter (also returned with fieldFov key)

	cursor = db.cursor()
	cursor.execute("SELECT fieldid, fieldra, fielddec FROM field")
	c = np.array(cursor.fetchall())
	RA = c[:,1]
	Dec = c[:,2]
	dbCoord = SkyCoord(ra = RA*units.degree, dec = Dec*units.degree, frame='icrs')
	inCoord = SkyCoord(ra = inRA*units.degree, dec = inDec*units.degree, frame='icrs')

	imin, sep2d, dist3d = match_coordinates_sky(inCoord, dbCoord)

	dbID = (c[imin,0]).astype('int') 

	mask = np.where(sep2d.to(units.degree).value > deglim)

	#this check apparently isn't necessary because it looks like the entire sky is covered with fieldIDs, but I suppose some of these fieldIDs don't have any observation dates (in the northern hemisphere)
	if (len(mask[0]) > 0):
		print("WARNING: coordinate outside LSST FOV", inRA[mask], inDec[mask])
		dbID[mask] = -999

	return dbID


if __name__ == '__main__':


	Nfields = 100
	myRA = np.random.rand(Nfields)*360.0 
	myDec = np.random.rand(Nfields)*180.0 - 90.0


	db = sqlite3.connect("minion_1016_sqlite.db")
	dbID = getFieldID(db, myRA, myDec)

	print(dbID)
