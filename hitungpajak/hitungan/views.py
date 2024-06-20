from django.shortcuts import render
from django.views import View
from .forms import Hitungan, CustomErr
from currencies import Currency
from random import randint
from django.http import JsonResponse
from django.views.decorators.http import require_POST




def testbug(request):
    return render(request, "testbug.html", {})
class Index(View):
    def get(self, request):
        form = Hitungan()
        return render(request, 'index.html', {'form':form})

    def post(self, request):  # Handle POST requests
        form = Hitungan(request.POST)
        try:
            if form.is_valid():
                # Handle form data here
                # ambil % bea masuk sesuai jenis produk
                jenis_barang = form.cleaned_data['jb']
                bea_masuk = 7.5
                if jenis_barang == 'tas':
                    bea_masuk = 20
                elif jenis_barang == 'tekstil':
                    bea_masuk = 25
                elif jenis_barang == 'sepatu':
                    bea_masuk = 30
                elif jenis_barang == 'lainnya':
                    bea_masuk = 7.5
                else:
                    print("Jenis produk tidak diketahui")

                nama_barang = form.cleaned_data['nama_barang']

                cost = form.cleaned_data['harga_barang']
                insurance = form.cleaned_data['nilai_asuransi']
                freight = form.cleaned_data['biaya_kirim']

                #hitung nilai import / CIF
                cif = cost + insurance + freight

                def hitung_dpp(cif,bea_masuk):
                    return (cif * bea_masuk) / 100
                def hitung_ppn(cif):
                    return (cif * 11) / 100
                def hitung_dppppn(dpp,ppn):
                    return  dpp + ppn

                dpp = hitung_dpp(cif,bea_masuk)
                ppn = hitung_ppn(cif)
                result = hitung_dppppn(dpp,ppn)




                formatted_cost = "{:,.2f}".format(cost)
                formatted_cost = (formatted_cost.replace('.', '|')
                                  .replace(',', '.').replace('|', ','))
                # print(formatted_cost)
                formatted_insurance = "{:,.2f}".format(insurance)
                formatted_insurance = (formatted_insurance.replace('.', '|')
                                       .replace(',', '.').replace('|', ','))
                formatted_freight = "{:,.2f}".format(freight)
                formatted_freight = (formatted_freight.replace('.', '|')
                                     .replace(',', '.').replace('|', ','))

                formatted_cif = "{:,.2f}".format(cif)
                formatted_cif = (formatted_cif.replace('.', '|')
                                 .replace(',', '.').replace('|', ','))

                formatted_dpp = "{:,.2f}".format(dpp)
                formatted_dpp = (formatted_dpp.replace('.', '|')
                                 .replace(',', '.').replace('|', ','))

                formatted_ppn = "{:,.2f}".format(ppn)
                formatted_ppn = (formatted_ppn.replace('.', '|')
                                 .replace(',', '.').replace('|', ','))

                formatted_result = "{:,.2f}".format(result)
                formatted_result = (formatted_result.replace('.', '|')
                                    .replace(',', '.').replace('|', ','))

                # Process the data, for example, save it to the database
                # Return a JsonResponse with any relevant data
                # return JsonResponse({'nama_barang': nama_barang, 'jenis_barang': jenis_barang,
                #                      'bea_masuk': bea_masuk, 'formatted_cost': formatted_cost,
                #                      'formatted_insurance': formatted_insurance, 'formatted_freight': formatted_freight,
                #                      'formatted_cif': formatted_cif, 'formatted_dpp': formatted_dpp,
                #                      'formatted_result': formatted_result})



                return render(request,'result.html',{'nama_barang': nama_barang, 'jenis_barang': jenis_barang,
                                     'bea_masuk': bea_masuk, 'formatted_cost': formatted_cost,
                                     'formatted_insurance': formatted_insurance, 'formatted_freight': formatted_freight,
                                     'formatted_cif': formatted_cif, 'formatted_dpp': formatted_dpp,
                                                     'formatted_result': formatted_result, 'formatted_ppn': formatted_ppn})
            else:
                return render(request, 'errorForm.html')
        except CustomErr as e:
            return render(request, 'errorForm.html', {'error_msg': e.message})









    # def post(self, request):
    #     #form = Hitungan(request.POST)
    #
    #     if request.method == "POST":
    #         form = Hitungan(request.POST)
    #         if form.is_valid():
    #             #temp = form.cleaned_data.get("harga_barang")
    #             print(type(form))
    #             print(form)
    #
    #
    #             #if form.is_valid():
    #             nama_barang = form.cleaned_data.get("nama_barang")
    #             jenis_barang = form.cleaned_data.get("jb")
    #             bea_masuk = 7.5
    #             cost = float(form.cleaned_data.get("harga_barang"))
    #             insurance = float(form.cleaned_data.get("nilai_asuransi"))
    #             freight = form.cleaned_data.get("biaya_kirim")
    #
    #             cif = cost + insurance + freight
    #             dpp = ((cif*bea_masuk)/100)*2
    #             result = (dpp*10)/100
    #
    #             #add currencies
    #             #format(cost,"0:12.2f")
    #             #print(type(cost))
    #             #cost = str(cost)
    #             #cost = cost.replace(".", ",")
    #             formatted_cost = "{:,.2f}".format(insurance)
    #             formatted_cost = (formatted_cost.replace('.', '|')
    #                               .replace(',', '.').replace('|', ','))
    #             #print(formatted_cost)
    #             formatted_insurance = "{:,.2f}".format(insurance)
    #             formatted_insurance = (formatted_insurance.replace('.', '|')
    #                               .replace(',', '.').replace('|', ','))
    #             formatted_freight = "{:,.2f}".format(freight)
    #             formatted_freight = (formatted_freight.replace('.', '|')
    #                                    .replace(',', '.').replace('|', ','))
    #
    #             formatted_cif = "{:,.2f}".format(cif)
    #             formatted_cif = (formatted_cif.replace('.', '|')
    #                                  .replace(',', '.').replace('|', ','))
    #
    #             formatted_dpp = "{:,.2f}".format(dpp)
    #             formatted_dpp = (formatted_dpp.replace('.', '|')
    #                              .replace(',', '.').replace('|', ','))
    #
    #             formatted_result = "{:,.2f}".format(result)
    #             formatted_result = (formatted_result.replace('.', '|')
    #                              .replace(',', '.').replace('|', ','))


        # tes function data pakai javascript
        # data = json.loads(request.body)
        # float_number = float(data['number'])
        # return JsonResponse({'float': f'You got: {float_number}'})

            #if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
               # number = randint(1,10)
              #  return JsonResponse({'number': number})

            #return render(request, 'index.html')

            # return render(request, 'result.html',{'hasil_akhir':formatted_result, 'bea_cukai':bea_masuk,
            #                                       'harga_barang':formatted_cost, 'nilai_asuransi':formatted_insurance,
            #                                       'biaya_kirim':formatted_freight, 'cif':formatted_cif, 'dpp':formatted_dpp,
            #                                       'nama_barang':nama_barang, 'jenis_barang':jenis_barang})
         #   total_result = form.cleaned_data['starting_amount']
          #  total_interest = 0
           ## yearly_results = {}

