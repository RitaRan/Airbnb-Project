from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired

class selecthouse:
    @staticmethod
    def form(amenities, houserules,
             checked_amens, checked_rules,
             in_street, in_district, in_zip_code,
             in_bookable, in_superhost,
             in_room_types_options, in_room_num_options, 
             in_bed_num_options,in_guest_num_options,
             cur_room_type, cur_room_num, cur_bed_num, cur_guest_num):
        class F(FlaskForm):
            street = StringField(default = in_street)
            district = StringField(default = in_district)
            zip_code = StringField(default = in_zip_code)
            selected_room_type = SelectField(u'selected room type', 
                choices = [(each_op, each_op) for each_op in in_room_types_options], default = cur_room_type)
            selected_room_num = SelectField(u'selected room num',
                choices = [(each_op, each_op) for each_op in in_room_num_options], default = cur_room_num)
            selected_bed_num = SelectField(u'selected bed num', 
                choices = [(each_op, each_op) for each_op in in_bed_num_options], default = cur_bed_num)
            selected_guest_num = SelectField(u'selected bed num', 
                choices = [(each_op, each_op) for each_op in in_guest_num_options], default = cur_guest_num)
            inst_bookable = BooleanField('Instant Bookable', default = True if in_bookable == '1' else False)
            super_host = BooleanField('Super Host', default = True if in_superhost == '1' else False) 

            @staticmethod
            def amen_field_name(index):
                return 'amen_{}'.format(index)
            def amen_fields(self):
                for i, amen in enumerate(amenities):
                    yield amen, getattr(self, F.amen_field_name(i))
            def get_amen_checked(self):
                for amen, field in self.amen_fields():
                    if field.data:
                        yield amen   

            @staticmethod
            def rule_field_name(index):
                return 'rule_{}'.format(index)
            def rule_fields(self):
                for i, rule in enumerate(houserules):
                    yield rule, getattr(self, F.rule_field_name(i))
            def get_rule_checked(self):
                for rule, field in self.rule_fields():
                    if field.data:
                        yield rule

        if checked_amens != "None":
            for i, amen in enumerate(amenities):
                field_name = F.amen_field_name(i)
                default = "checked" if amen in checked_amens else None
                setattr(F, field_name, BooleanField(default=default))
            for i, rule in enumerate(houserules):
                field_name = F.rule_field_name(i)
                default = "checked" if rule in checked_rules else None
                setattr(F, field_name, BooleanField(default=default))
        else:
            for i, amen in enumerate(amenities):
                field_name = F.amen_field_name(i)
                default = None
                setattr(F, field_name, BooleanField(default=default))
            for i, rule in enumerate(houserules):
                field_name = F.rule_field_name(i)
                default = None
                setattr(F, field_name, BooleanField(default=default))
        return F()