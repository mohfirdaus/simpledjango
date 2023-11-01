# Generated by Django 4.2.6 on 2023-11-01 08:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BukuTabungan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namabank', models.CharField(choices=[('BCA', 'BCA'), ('BRI', 'BRI'), ('BNI', 'BNI')], max_length=6)),
            ],
        ),
        migrations.RemoveField(
            model_name='mahasiswa',
            name='id',
        ),
        migrations.AlterField(
            model_name='mahasiswa',
            name='nim',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Transaksi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipetransaksi', models.CharField(choices=[('Setor', 'Setor'), ('Tarik', 'Tarik')], max_length=10)),
                ('nominal', models.DecimalField(decimal_places=0, max_digits=10)),
                ('tanggal', models.DateTimeField(default=django.utils.timezone.now)),
                ('related_bukutabungan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='form.bukutabungan')),
            ],
        ),
        migrations.AddField(
            model_name='bukutabungan',
            name='namapemilik',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.mahasiswa'),
        ),
    ]