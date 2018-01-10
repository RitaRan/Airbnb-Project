from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, DateTimeField, SelectField
from wtforms.validators import DataRequired

class selecthouse:
    @staticmethod
    def form(amenities,checked_amen,
            house_rules, checked_rules,
            in_address, in_min_price, in_max_price,
            in_check_in, in_check_out,
            in_bookable,
            in_room_types_options, in_bed_num_options, in_guest_num_options,
            cur_room_type, cur_bed_num , cur_guest_num,
            lst_crime_rate,
            c_shop, c_rest):
        class F(FlaskForm):
            address = StringField(default = in_address)
            check_in = StringField(default = in_check_in)
            check_out = StringField(default = in_check_out)
            min_price = StringField(default = in_min_price)
            max_price = StringField(default = in_max_price)
            selected_room_type = SelectField(u'selected room type', 
                                             choices = [(each_op, each_op) for each_op in in_room_types_options], 
                                             default = cur_room_type)
            selected_bed_num = SelectField(u'selected bed num', 
                                           choices = [(each_op, each_op) for each_op in in_bed_num_options], 
                                           default = cur_bed_num)
            selected_guest_num = SelectField(u'selected bed num', 
                                             choices = [(each_op, each_op) for each_op in in_guest_num_options], 
                                             default = cur_guest_num)
            inst_bookable = BooleanField('Instant Bookable', 
                                         default = True if in_bookable == '1' else False)
            # preference - crime
            lowest_crime_rate = BooleanField('Lowest Crime Rate', 
                                             default = True if lst_crime_rate == '1' else False)
            close_shop = BooleanField('Closest to Shopping Center', 
                                             default = True if c_shop == '1' else False)
            close_rest = BooleanField('Closest to Restaurant', 
                                             default = True if c_rest == '1' else False)

            # amenties 
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
            # house rules 
            def rule_field_name(index):
                return 'rule_{}'.format(index)
            def rule_fields(self):
                for i, rule in enumerate(house_rules):
                    yield rule, getattr(self, F.rule_field_name(i))
            def get_rule_checked(self):
                for rule, field in self.rule_fields():
                    if field.data:
                        yield rule
           

        # amenties 
        if checked_amen != "None":
            for i, amen in enumerate(amenities):
                field_name = F.amen_field_name(i)
                default = "checked" if amen in checked_amen else None
                setattr(F, field_name, BooleanField(default=default))

            # house rules 
            for i, rule in enumerate(house_rules):
                field_name = F.rule_field_name(i)
                default = "checked" if rule in checked_rules else None
                setattr(F, field_name, BooleanField(default=default))


        else:
            for i, _ in enumerate(amenities):
                field_name = F.amen_field_name(i)
                default = None
                setattr(F, field_name, BooleanField(default=default))
            for i, _ in enumerate(house_rules):
                field_name = F.rule_field_name(i)
                default = None
                setattr(F, field_name, BooleanField(default=default))


        return F()
