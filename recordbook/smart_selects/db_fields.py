from django.db.models.fields.related import ForeignKey
import form_fields

class ChainedForeignKey(ForeignKey):
    """
    chains the choices of a previous combo box with this one
    """
    def __init__(self, to, chained_field, chained_model_field, *args, **kwargs):
        self.app_name = to._meta.app_label
        self.model_name = to._meta.object_name
        self.chain_field = chained_field
        self.model_field = chained_model_field
        ForeignKey.__init__(self, to, *args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': form_fields.SimpleChainedModelChoiceField,
            'queryset': self.rel.to._default_manager.complex_filter(self.rel.limit_choices_to),
            'to_field_name': self.rel.field_name,
            'app_name': self.app_name,
            'model_name': self.model_name,
            'chain_field': self.chain_field,
            'model_field': self.model_field,
        }
        defaults.update(kwargs)
        return super(ChainedForeignKey, self).formfield(**defaults)

class SimpleChainedForeignKey(ChainedForeignKey):
    pass

class GroupedForeignKey(ForeignKey):
    """
    Opt Grouped Field
    """
    def __init__(self, to, group_field, *args, **kwargs):
        self.group_field = group_field
        self._choices = True
        ForeignKey.__init__(self, to, *args, **kwargs)
    
    def formfield(self, **kwargs):
        defaults = {
            'form_class': form_fields.GroupedModelSelect,
            'queryset': self.rel.to._default_manager.complex_filter(
                                                    self.rel.limit_choices_to),
            'to_field_name': self.rel.field_name,
            'order_field': self.group_field,
        }
        defaults.update(kwargs)
        return super(ForeignKey, self).formfield(**defaults)

