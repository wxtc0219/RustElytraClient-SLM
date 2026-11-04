import os, sys, zipfile

src, repdir, dst = sys.argv[1:4]
zin = zipfile.ZipFile(src, 'r')
zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
replaced = []
for item in zin.infolist():
    data = zin.read(item.filename)
    cand = os.path.join(repdir, item.filename)
    if os.path.isfile(cand):
        data = open(cand, 'rb').read()
        replaced.append(item.filename)
    zout.writestr(item, data)
zout.close()
zin.close()
print('replaced:', replaced)
print('output:', dst, os.path.getsize(dst), 'bytes', len(zipfile.ZipFile(dst).namelist()), 'entries')
