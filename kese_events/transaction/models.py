from django.db import models
from core.mixins import BaseModelMixin, NULL
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from events.models import Event
from authentication.models import UserProfile
import qrcode
from PIL import Image
from io import BytesIO

from transaction.chapa.models import ChapaTransaction

class PaymentMethodChoices(models.TextChoices):
    AMOLE = 'amole', 'AMOLE'
    HELLO_CASH = 'hello_cash', 'HELLO_CASH'
    TELLE_BIRR = 'telle_birr', 'TELLE_BIRR'
    CHAPA = 'chapa', 'CHAPA'

class AttendanceMethodChoices(models.TextChoices):
    INPERSON = 'inperson', 'INPERSON'
    ONLINE = 'online', 'ONLINE'

class TicketTransaction(BaseModelMixin):
    # chapa_transaction = models.ForeignKey(ChapaTransaction, on_delete=models.DO_NOTHING, related_name='ticket_transaction')
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, related_name='transactions')
    user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name='tickets')
    payment_method = models.CharField(max_length=255, choices=PaymentMethodChoices.choices, default=PaymentMethodChoices.CHAPA)
    attendance_method = models.CharField(max_length=255, choices=AttendanceMethodChoices.choices, default=AttendanceMethodChoices.INPERSON)
    is_vip = models.BooleanField(default=False)
    Quantity = models.IntegerField(default=1)
    TotalPrice = models.IntegerField(default=0)
    qr_code = models.ImageField(upload_to='ticket_qr_codes/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.qr_code:
            # Generate a unique QR code content based on ticket details
            qr_code_content = f"Event: {self.event.title}, "
            qr_code_content += f"Location: {self.event.location}, "
            qr_code_content += f"Start Date: {self.event.start_date}, "
            qr_code_content += f"End Date: {self.event.end_date}, "
            qr_code_content += f"Ticket Type: {'VIP' if self.is_vip else 'Regular'}, "
            qr_code_content += f"User: {self.user.first_name} {self.user.last_name}, "
            qr_code_content += f"Payment Method: {self.get_payment_method_display()}, "
            qr_code_content += f"Attendance Method: {self.get_attendance_method_display()}, "
            qr_code_content += f"Quantity: {self.Quantity}, "
            qr_code_content += f"Total Price: {self.TotalPrice}"
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_code_content)
            qr.make(fit=True)

            # Create a QR code image
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_io = BytesIO()
            qr_img.save(qr_io, format='PNG')
            qr_io.seek(0)

            self.qr_code.save(f'ticket_{self.id}.png', SimpleUploadedFile(f'ticket_{self.id}.png', qr_io.read(), content_type='image/png'))
            super().save(update_fields=['qr_code'])
