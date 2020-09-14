# desk_qrcode_creator
This is a desk App for Neuron to generate qrCode files

### Add a new python module in project
```python
python3 -m pip install -r requirements.txt
```

### build the app
```python
pyinstaller --windowed --onefile --icon=logo.ico --noconfirm main.py

#pyinstaller --windowed --onefile --noconfirm --icon=logo.ico main.spec
```