from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Mahasiswa(models.Model):
    nama = models.CharField(max_length=255)
    nim = models.PositiveIntegerField(primary_key=True)
    alamat = models.TextField()
    foto = models.ImageField(upload_to='foto_mahasiswa', blank=True, null=True)

    def __str__(self):
        return self.nama
    
    def get_absolute_url(self):
        return reverse("listmahasiswa")
    
class BukuTabungan(models.Model):
    BANK = (
        ('BCA', 'BCA'),
        ('BRI', 'BRI'),
        ('BNI', 'BNI'),
    )
    namapemilik = models.ForeignKey("Mahasiswa", on_delete=models.CASCADE,)
    namabank = models.CharField(max_length=6, choices=BANK,)

    def __str__(self):
        return f"{self.namapemilik.nama} di Bank {self.namabank}"
    
    def get_absolute_url(self):
        return reverse("listbukutabungan")
    
class Transaksi(models.Model):
    TRANSACTION_TYPES = (
        ('Setor', 'Setor'),
        ('Tarik', 'Tarik'),
    )
    related_bukutabungan = models.ForeignKey(BukuTabungan, on_delete=models.CASCADE, null=True, blank=True)
    tipetransaksi = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    nominal = models.DecimalField(max_digits=10, decimal_places=0)
    tanggal = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.tipetransaksi} oleh {self.related_bukutabungan.namapemilik.nama} pada {self.tanggal}"
