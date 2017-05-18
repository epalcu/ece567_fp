from concurrent.futures import ProcessPoolExecutor
import collections
import xlrd
import sys
import time

sys.stderr.write("Opening workbook..\n")

# Start taking time, bruh..
start = time.time()

# Open Excel file
workbook = xlrd.open_workbook("Vehicles2006-2011.xlsx")

sys.stderr.write("Opening sheet..\n")

# Specify sheet within file to open
sheet = workbook.sheet_by_name("all car fires 2006-2011")

# Dictionary of makes that we care about..
makes = {"Chevrolet": {"year": [], "origin": []},
         "Dodge": {"year": [], "origin": []},
         "Ford": {"year": [], "origin": []}
         }

num_rows = sheet.nrows

origin = 21
make = 35
year = 37

sys.stderr.write("Populating dictionary..\n")

# Traverse across rows
for row in range(1, num_rows):
    # If make is a Chevrolet
    if (sheet.cell(row, make).value == "CH"):
        try:
            year_val = int(sheet.cell(row, year).value)
            origin_val = str(sheet.cell(row, origin).value)

            # Convert "undetermined" to 100
            if (origin_val == "UU"):
                origin_val = "100"

            # Make sure year and origin data exist
            if (year_val != xlrd.empty_cell.value and origin_val != xlrd.empty_cell.value):
                # Add model year to "Chevrolet" key within dictionary of makes
                makes["Chevrolet"]["year"].append(year_val)
                # Add model origin to "Chevrolet" key within dictionary of makes
                makes["Chevrolet"]["origin"].append(int(float(origin_val)))
        except:
            continue

    # If make is a Ford
    elif (sheet.cell(row, make).value == "DO"):
        try:
            year_val = int(sheet.cell(row, year).value)
            origin_val = str(sheet.cell(row, origin).value)

            # Convert "undetermined" to 100
            if (origin_val == "UU"):
                origin_val = 100

            # Make sure year and origin data exist
            if (year_val != xlrd.empty_cell.value and origin_val != xlrd.empty_cell.value):
                # Add model year to "Dodge" key within dictionary of makes
                makes["Dodge"]["year"].append(year_val)
                # Add model origin to "Dodge" key within dictionary of makes
                makes["Dodge"]["origin"].append(int(float(origin_val)))
        except:
            continue

    # If make is a Ford
    elif (sheet.cell(row, make).value == "FO"):
        try:
            year_val = int(sheet.cell(row, year).value)
            origin_val = str(sheet.cell(row, origin).value)

            # Convert "undetermined" to 100
            if (origin_val == "UU"):
                origin_val = 100

            # Make sure year and origin data exist
            if (year_val != xlrd.empty_cell.value and origin_val != xlrd.empty_cell.value):
                # Add model year to "Ford" key within dictionary of makes
                makes["Ford"]["year"].append(year_val)
                # Add model origin to "Ford" key within dictionary of makes
                makes["Ford"]["origin"].append(int(float(origin_val)))
        except:
            continue

sys.stderr.write("Writing to files..\n")

# Write makes dictionary to files:
# Contained in the "samples.csv" are "Make, year"
# Contained in the "targets.csv" are the fire origins

# Write Chevy data
def write_chevy(items):
    for key, value in items:
        for val in value:
            if (key == "year"):
                open("ml/samples.csv", 'a+').write("{0}, {1}\n".format(1000, val))
            else:
                open("ml/targets.csv", 'a+').write("{0}\n".format(val))

# Write Dodge data
def write_dodge(items):
    for key, value in items:
        for val in value:
            if (key == "year"):
                open("ml/samples.csv", 'a+').write("{0}, {1}\n".format(1001, val))
            else:
                open("ml/targets.csv", 'a+').write("{0}\n".format(val))

# Write Ford data
def write_ford(items):
    for key, value in items:
        for val in value:
            if (key == "year"):
                open("ml/samples.csv", 'a+').write("{0}, {1}\n".format(1002, val))
            else:
                open("ml/targets.csv", 'a+').write("{0}\n".format(val))

# Parallelize the writing of the dictionary..one worker process per dictionary key
with ProcessPoolExecutor(max_workers=3) as e:
    e.submit(write_chevy, makes["Chevrolet"].items())
    e.submit(write_dodge, makes["Dodge"].items())
    e.submit(write_ford, makes["Ford"].items())

# End the time
end = time.time() - start
sys.stderr.write("Total elapsed time: {0}.\n".format(round(end, 2)))
exit()
