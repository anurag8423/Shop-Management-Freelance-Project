from .models import FirmInfo

def firm_info(request):
    try:
        firm_info = FirmInfo.objects.first()
        return {
            'firm_name': firm_info.firm_name if firm_info else 'Default Firm Name',
            'firm_image_url': firm_info.firm_image.url if firm_info and firm_info.firm_image else None,
            'firm_gst':firm_info.firm_gst if firm_info else '10FZXPP1309C1Z1',
            'firm_mob1':firm_info.firm_mob1 if firm_info else '8210463930',
            'firm_mob2':firm_info.firm_mob2 if firm_info else '9708805703',
            'firm_add':firm_info.firm_add if firm_info else 'No address'

        }
    except FirmInfo.DoesNotExist:
        return {
            'firm_name': 'Default Firm Name',
            'firm_image_url': None
        }
