import os, zipfile, shutil
ziplist = []
n = 1
counter = 0

rootdir = os.getcwd()
# Read folder/file names
try:
    for name in os.listdir(rootdir):
        if ".zip" in name:
            ziplist.append(name)
except:
    print("\n !! The entered file path is not found !!\n")
    rootdir = input("Enter the file path of the folder containing the images (e.g. C:\\TriageImages\\Company): ")
    for name in os.listdir(rootdir):
        if ".zip" in name:
            ziplist.append(name)

# Read individual zip file
for zipname in ziplist:
    status = set()
    # Zip file handler
    zip = zipfile.ZipFile(rootdir + "\\" + zipname)
    print (n)
    print (zipname)
    n += 1

    # Going up one directory
    drivedir = rootdir.split("\\", 1)[0]
    companydir = rootdir.rsplit("\\", 1)[1]
    # Target folder name: Company name\zip file name\
    dirname = drivedir + "\\Output\\" + companydir + "\\" + zipname[:-4] + "\\NTDS"
    dirname2 = drivedir + "\\Output\\" + companydir + "\\" + zipname[:-4] + "\\config"

    # Read individual files in one zip file
    for filepath in zip.namelist():
        if ".vhdx" in filepath or ".vhd" in filepath:
            status.add("KAPE")

        elif "Windows/NTDS" in filepath:
            status.add("Windows/NTDS")
            # Create folder
            if counter == 0:
                print("Windows/NTDS exists. \n")
                print("Starting extraction... ")
                try:
                    os.makedirs(dirname)
                    os.makedirs(dirname2)

                except:
                    print("\n !! The following folders already exist !! \n" + dirname + " and/or \n" + dirname2 + "\n")
                    dirname = input("Please create a new path for NTDS files (e.g. C:\\Users\\NatalieY\\Downloads\\Company\\NTDS): ")
                    dirname2 = input("Please create a new path for config files (e.g. C:\\Users\\NatalieY\\Downloads\\Company\\config): ")
                    os.makedirs(dirname)
                    os.makedirs(dirname2)
            counter += 1

            # copy file (taken from zipfile's extract)
            source = zip.open(filepath)
            target = open(os.path.join(dirname, filepath.replace("/", "\\").rsplit("\\", 1)[1]), "wb")
            try:
                shutil.copyfileobj(source, target)
                print("Extracted --- ", filepath)
            except:
                print("!! Problem extracting !! --- ", filepath)

        elif "System32/config" in filepath and "Windows/NTDS" in status:
            status.add("System32/config")

            filepathExtend = filepath.rsplit("C/Windows/System32/config", 1)[1]

            if filepathExtend.count("/") > 1:
                dirnameExtend = dirname2 + filepathExtend.replace("/", "\\").rsplit("\\", 1)[0]
                try:
                    # Create subfolders
                    os.makedirs(dirnameExtend)
                except:
                    pass
                # Copy file (taken from zipfile's extract)
                source = zip.open(filepath)
                target = open(os.path.join(dirnameExtend, filepath.replace("/", "\\").rsplit("\\", 1)[1]), "wb")
                try:
                    shutil.copyfileobj(source, target)
                    print("Extracted --- ", filepath)
                except:
                    print("!! Problem extracting !! --- ", filepath)

            else:
                # Copy file (taken from zipfile's extract)
                source = zip.open(filepath)
                target = open(os.path.join(dirname2, filepath.replace("/", "\\").rsplit("\\", 1)[1]), "wb")
                try:
                    shutil.copyfileobj(source, target)
                    print("Extracted --- ", filepath)
                except:
                    print("!! Problem extracting !! --- ", filepath)

        else:
            continue

    if "KAPE" in status:
        print ("It is a KAPE image.")

    elif "Windows/NTDS" in status and "System32/config" in status:
        print ("--- NTDS & System32/config extraction completed. ---")
        print("\n The following folders are created: \n" + dirname + " and \n" + dirname2 + "\n")

    else:
        print("No .vhdx, .vhd or Windows/NTDS found in the image.")