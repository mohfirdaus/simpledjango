from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from form.models import Mahasiswa, BukuTabungan, Transaksi
from form.forms import NewUserForm, BukuTabunganForm, TransaksiForm, UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect


# Create your views here.
def register(request):
    page_title = "Registration Page"
    next_url = request.GET.get('next', 'home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form,'page_title':page_title})

# class YourCustomLoginView(LoginView):
#     def form_valid(self, form):
#         # Get the 'next' parameter from the request GET parameters
#         redirect_to = self.request.GET.get('next', '')
#         print(f"Redirect to: {redirect_to}")
        
#         if redirect_to:
#             return HttpResponseRedirect(redirect_to)  # Redirect to the 'next' parameter if it's provided
#         else:
#             return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class CreateFormMahasiswa(CreateView):
    template_name='mahasiswa.html'
    form_class = NewUserForm
    model = Mahasiswa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Tambah Mahasiswa'  # Set the title in the context
        return context

@method_decorator(login_required, name='dispatch')
class UpdateFormMahasiswa(UpdateView):
    template_name = 'mahasiswa.html'
    form_class = NewUserForm
    model = Mahasiswa

@method_decorator(login_required, name='dispatch')
class DeleteFormMahasiswa(DeleteView):
    model = Mahasiswa
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy("listmahasiswa")

@method_decorator(login_required, name='dispatch')
class ListMahasiswa(ListView):
    model = Mahasiswa
    template_name = 'list.html'
    context_object_name = 'listmahasiswa'

    def get_queryset(self):
        return Mahasiswa.objects.all().order_by('-pk')
    
#########################################
#########################################

@method_decorator(login_required, name='dispatch')
class CreateFormBukuTabungan(CreateView):
    template_name = "buku_tabungan.html"
    form_class = BukuTabunganForm
    model = BukuTabungan

@method_decorator(login_required, name='dispatch')
class UpdateFormBukuTabungan(UpdateView):
    template_name = 'buku_tabungan.html'
    form_class = BukuTabunganForm
    model = BukuTabungan

class ListBukuTabungan(ListView):
    model = BukuTabungan
    template_name = 'list_buku_tabungan.html'
    context_object_name = 'listbukutabungan'

    def get_queryset(self):
        return BukuTabungan.objects.all().order_by('-pk')

@method_decorator(login_required, name='dispatch')   
class DeleteBukuTabungan(DeleteView):
    model = BukuTabungan
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy("listbukutabungan")

#########################################
#########################################
@login_required
def buat_transaksi(request, bukutabungan_pk):
    page_title = "Buat Transaksi Tabungan"
    bukutabungan = BukuTabungan.objects.get(pk=bukutabungan_pk)

    if request.method == 'POST':
        form = TransaksiForm(bukutabungan_pk, data=request.POST)
        if form.is_valid():
            transaksi = form.save(commit=False)
            transaksi.related_bukutabungan = bukutabungan
            transaksi.save()
            return redirect('listtransaksi', bukutabungan_pk=bukutabungan_pk)

    else:
        form = TransaksiForm(bukutabungan_pk)

    return render(request, 'transaksi.html', {'form': form, 'bukutabungan': bukutabungan, 'page_title':page_title})

@login_required
def list_transaksi(request, bukutabungan_pk):
    page_title = "List Transaksi Tabungan"
    bukutabungan = BukuTabungan.objects.get(pk=bukutabungan_pk)
    transaksi_list = Transaksi.objects.filter(related_bukutabungan=bukutabungan).order_by('-tanggal')

    saldo = 0
    for transaksi in transaksi_list:
        if transaksi.tipetransaksi == 'Setor':
            saldo += int(transaksi.nominal)
        elif transaksi.tipetransaksi == 'Tarik':
            saldo -= int(transaksi.nominal)

    return render(request, 'list_transaksi.html', {'transaksi_list': transaksi_list, 'bukutabungan' : bukutabungan, 'saldo':saldo, 'paga_title':page_title})
    