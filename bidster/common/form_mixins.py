class DefaultFormMixin():
    def __init_fields__(self, *args, **kwargs):
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += ' form__input '
