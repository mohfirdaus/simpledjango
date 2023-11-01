from django import forms
from form.models import Mahasiswa, BukuTabungan, Transaksi
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        error_messages={
            'required': 'Please enter your username.',
            'unique': 'This username is already taken.',
        }
    )
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class NewUserForm(forms.ModelForm):
    class Meta():
        model = Mahasiswa
        fields = '__all__'
        
    nama = forms.CharField(
        label='Nama Lengkap',
        widget=forms.TextInput(attrs={'placeholder': 'Masukkan Nama Lengkap', 'class': 'form-control'})
    )
    nim = forms.CharField(
        label='NIM',
        widget=forms.TextInput(attrs={'placeholder': 'Masukkan NIM', 'class': 'form-control'})
    )
    alamat = forms.CharField(
        label='Alamat',
        widget=forms.Textarea(attrs={'placeholder': 'Masukkan Alamat', 'class': 'form-control'})
    )
    foto = forms.ImageField(
        label='Foto',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    

class BukuTabunganForm(forms.ModelForm):
    namapemilik = forms.ModelChoiceField(
        queryset=Mahasiswa.objects.all(),
        label='Nama Pemilik Rekening',
        widget=forms.Select(attrs={'class': 'form-control'})  # Menyesuaikan widget untuk nama pemilik
    )

    namabank = forms.ChoiceField(
        choices=[('', 'Pilih Bank Anda')] + list(BukuTabungan.BANK),
        label='Nama Bank',
        widget=forms.Select(attrs={'class': 'form-control'})  # Menyesuaikan widget untuk nama bank
    )

    def __init__(self, *args, **kwargs):
        super(BukuTabunganForm, self).__init__(*args, **kwargs)
        self.fields['namapemilik'].label_from_instance = lambda obj: f"{obj.nim} - {obj.nama}"

    class Meta:
        model = BukuTabungan
        fields = ['namapemilik', 'namabank']
        labels = {
            'namabank': 'Nama Bank',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        namapemilik = cleaned_data.get('namapemilik')
        namabank = cleaned_data.get('namabank')

        if namapemilik and namabank:
            existing_count = BukuTabungan.objects.filter(namapemilik=namapemilik, namabank=namabank).count()
            if existing_count > 0:
                raise ValidationError(f"{namapemilik} sudah memiliki bank {namabank}.")
        return cleaned_data
    
class TransaksiForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['tipetransaksi', 'nominal']

    def __init__(self, bukutabungan_pk, *args, **kwargs):
        super(TransaksiForm, self).__init__(*args, **kwargs)

        bukutabungan = BukuTabungan.objects.get(pk=bukutabungan_pk)

        # self.fields['related_bukutabungan'].disabled = True

        # self.fields['related_bukutabungan'].label = 'Nama: ' + bukutabungan.namapemilik.nama

        # self.fields['related_bukutabungan'].widget = forms.TextInput(attrs={'style': 'display:none'})

        self.fields['tipetransaksi'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Tipe Transaksi'})
        self.fields['nominal'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nominal'})
        self.fields['nominal'].label = 'Jumlah Nominal'
        self.fields['tipetransaksi'].label = 'Tipe Transaksi'

