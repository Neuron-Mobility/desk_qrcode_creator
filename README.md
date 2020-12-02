# desk_qrcode_creator
This is a desk App for Neuron to generate qrCode files

### Add a new python module in project
```python
python3 -m pip install -r requirements.txt
```

### build the Mac app
```shell script
pyi-makespec -w -F -i=logo-mac.icns --add-data=static:static --osx-bundle-identifier=com.neuronride.qrcode-creator -n mac_qrcode_creator main.py

pyinstaller -w -F --clean --noconfirm mac_qrcode_creator.spec
```

### build the Window app
```shell script
pyi-makespec -w -F -i=logo-win.ico --add-data=static;static -n win_qrcode_creator main.py

pyinstaller -w -c -F --clean --noconfirm win_qrcode_creator.spec
```

if permission denied:
```shell script
sudo rm -rf /Users/leng/Library/Application\ Support/pyinstaller/bincache00_py38_64bit/*
```