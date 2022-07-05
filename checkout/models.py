from django.db import models


class DeliveryOptions(models.Model):
    """
    The Delivery methods table contining all delivery
    """

    DELIVERY_CHOICES = [
        ("SP", "Store Pick-Up"),
        ("HD", "Home Delivery"),
    ]

    delivery_name = models.CharField(
        verbose_name="delivery_name",
        help_text="Required",
        max_length=255,
    )
    delivery_price = models.DecimalField(
        verbose_name="delivery price",
        help_text="Maximum 999.99",
        error_messages={
            "name": {
                "max_length": "The price must be between 0 and 999.99.",
            },
        },
        max_digits=5,
        decimal_places=2,
    )

    delivery_method = models.CharField(null=True,
                                       choices=DELIVERY_CHOICES,
                                       verbose_name="delivery_method",
                                       help_text="Required",
                                       max_length=255,
                                       )

    delivery_timeframe = models.CharField(
        verbose_name="delivery timeframe",
        help_text="Required",
        max_length=255,
    )
    delivery_window = models.CharField(
        verbose_name="delivery window",
        help_text="Required",
        max_length=255,
    )
    order = models.IntegerField(
        verbose_name="list order", help_text="Required", default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Delivery Option"
        verbose_name_plural = "Delivery Options"

    def __str__(self):
        return self.delivery_name


class PaymentSelections(models.Model):
    """
    Store payment options
    """

    name = models.CharField(
        verbose_name="name",
        help_text="Required",
        max_length=255,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Payment Selection"
        verbose_name_plural = "Payment Selections"

    def __str__(self):
        return self.name
