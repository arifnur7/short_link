from django import forms

jenis_barang= [
    ('tas', 'Tas/ Koper / sejenisnya'),
    ('tesktil', 'Tekstil / Garmen/ sejenisnya'),
    ('sepatu', 'Alas kaki/ Sepatu / sejenisnya'),
    ('buku', 'Buku'),
    ('lainnya','Lainnya'),
    ]
class Hitungan(forms.Form):
    nama_barang = forms.CharField(
        label = 'Nama Produk/Barang',
        max_length = 100,
        widget = forms.TextInput(
            attrs = {
                'class':'form-control',
                'placeholder':'Masukkan Nama Produk / Barang',
            }
        )
    )
    jb = forms.ChoiceField(
        label = 'Jenis Produk / Barang',
        choices = [
                    ('tas', 'Tas/ Koper / sejenisnya'),
                    ('tesktil', 'Tekstil / Garmen/ sejenisnya'),
                    ('sepatu', 'Alas kaki/ Sepatu / sejenisnya'),
                    ('buku', 'Buku'),
                    ('lainnya','Lainnya'),
                    ],
        widget= forms.Select(
            attrs={
                'class':'form-control'
            }
        )

    )

    harga_barang = forms.FloatField(
        label = 'Harga Produk/Barang',
        widget = forms.NumberInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'Masukkan Harga Produk / Barang'
            }
        )
    )
    nilai_asuransi = forms.FloatField(
        label='Nilai Asuransi',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan Nilai Asuransi'
            }
        )
    )
    biaya_kirim = forms.FloatField(
        label='Biaya Pengiriman',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan Biaya Kirim'
            }
        )
    )
    #jenis_barang = forms.CharField()

    def clean(self):
        cleaned_data=super().clean()
        nama_barang=self.cleaned_data['nama_barang']
        if len(nama_barang) <3:
            raise CustomErr("Nama Barang kurang dari 3 Huruf")
        harga_barang = self.cleaned_data['harga_barang']
        if harga_barang < 10:
            raise CustomErr("Harga Barang kurang dari 2 Karakter")
        nilai_asuransi = self.cleaned_data['nilai_asuransi']
        if nilai_asuransi < 10:
            raise CustomErr("Nilai Asuransi kurang dari 2 Karakter")
        biaya_kirim = self.cleaned_data['biaya_kirim']
        if biaya_kirim < 10:
            raise CustomErr("Biaya Kirim kurang dari 10 USD ")

class CustomErr(Exception):
    def __init__(self, message):
        self.message = message
