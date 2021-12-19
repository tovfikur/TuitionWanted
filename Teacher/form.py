from django import forms
from .models import Teacher


class TeacherRegistrationForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TeacherRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['Name'].widget.attrs['placeholder'] = 'Type your name'
        self.fields['Email'].widget.attrs['placeholder'] = 'tuitionwantedbangladesh@gmail.com'
        self.fields['Email'].widget.attrs['style'] = 'width:100%'
        self.fields['Phone'].widget.attrs['placeholder'] = 'Your phone number'
        self.fields['Password'].widget.attrs['placeholder'] = 'Set any password'
        self.fields['Facebook_Link'].widget.attrs['placeholder'] = 'https://www.facebook.com/TuitionWantedcom'
        self.fields['Refer_Name'].widget.attrs['placeholder'] = 'Local guardian name'
        self.fields['BloodGroup'].widget.attrs['style'] = ' font-size: 16px;'
        self.fields['Age'].widget.attrs['style'] = ' font-size: 16px;'
        self.fields['Religion'].widget.attrs['style'] = ' font-size: 16px;'
        self.fields['Gender'].widget.attrs['style'] = ' font-size: 16px;'
        self.fields['Type'].widget.attrs['style'] = ' font-size: 16px;'

        self.fields['SSC_Institute'].widget.attrs['placeholder'] = 'Type your school name'
        self.fields['SSC_Subject'].widget.attrs['style'] = 'width: 30%; font-size: 16px;'
        self.fields['SSC_MEDIUM'].widget.attrs['style'] = 'width: 30%; font-size: 16px;'
        self.fields['SSC_GPA'].widget.attrs['style'] = 'width: 70%; font-size: 16px;'
        self.fields['SSC_GPA'].widget.attrs['placeholder'] = 'GPA'
        self.fields['SSC_GOLDEN'].widget.attrs['style'] = 'width: 30%; font-size: 16px;'
        self.fields['SSC_Year'].widget.attrs['style'] = 'width: 30%; font-size: 16px;'
        self.fields['SSC_MEDIUM_Curriculum'].widget.attrs['style'] = 'width: 30%;'

        self.fields['HSC_Institute'].widget.attrs['placeholder'] = 'Type your college name'
        self.fields['HSC_Subject'].widget.attrs['style'] = 'width: 30%; font-size: 16px;'
        self.fields['HSC_MEDIUM'].widget.attrs['style'] = 'width: 30%; font-size: 16px;'
        self.fields['HSC_GPA'].widget.attrs['style'] = 'width: 70%; font-size: 16px;'
        self.fields['HSC_GPA'].widget.attrs['placeholder'] = 'GPA'
        self.fields['HSC_GOLDEN'].widget.attrs['style'] = 'width: 30%; font-size: 16px;'
        self.fields['HSC_Year'].widget.attrs['style'] = 'width: 30%; font-size: 16px;'
        self.fields['HSC_MEDIUM_Curriculum'].widget.attrs['style'] = 'width: 30%;'

        self.fields['Graduation_Institute'].widget.attrs['style'] = 'width: 30%; font-size: 16px;'
        self.fields['Graduation_Subject'].widget.attrs['style'] = 'width: 30%; font-size: 16px;'
        self.fields['Graduation_GPA'].widget.attrs['style'] = 'width: 70%; font-size: 16px;'
        self.fields['Graduation_GPA'].widget.attrs['placeholder'] = 'CGPA'
        self.fields['Graduation_Year'].widget.attrs['style'] = 'width: 30%; font-size: 16px;'

        self.fields['Post_Graduation_Institute'].widget.attrs['style'] = 'width: 30%; font-size: 16px;'
        self.fields['Post_Graduation_Subject'].widget.attrs['style'] = 'width: 30%; font-size: 16px;'
        self.fields['Post_Graduation_GPA'].widget.attrs['style'] = 'width: 70%; font-size: 16px;'
        self.fields['Post_Graduation_GPA'].widget.attrs['placeholder'] = 'CGPA'
        self.fields['Post_Graduation_Year'].widget.attrs['style'] = 'width: 30%; font-size: 16px;'

        self.fields['TuitionStyle'].widget.attrs['style'] = ' font-size: 16px;'
        self.fields['ExpectedSalary'].widget.attrs['style'] = 'width: 100%; font-size: 16px;'
        self.fields['Experience'].widget.attrs['style'] = 'width: 100%; font-size: 16px;'
        self.fields['Preferred'].widget.attrs['style'] = 'width: 100%; font-size: 16px;'
        self.fields['Expertise'].widget.attrs['style'] = 'width: 100%; font-size: 16px;'
        self.fields['Expertise'].widget.attrs['placeholder'] = 'Ex: Photoshop, Exel,Programming Etc. (Any)'
        self.fields['HandWriting'].widget.attrs['style'] = ' font-size: 16px;'
        self.fields['Running_Tuition'].widget.attrs['style'] = 'width: 100%; font-size: 16px;'

        self.fields['Avatar'].widget.attrs['onchange'] = 'avaloadFile(event)'
        self.fields['NID'].widget.attrs['onchange'] = 'nidloadFile(event)'
        self.fields['NID'].widget.attrs['onchange'] = 'nidloadFile(event)'
        self.fields['StudentID'].widget.attrs['onchange'] = 'sidloadFile(event)'
        self.fields['Certificate'].widget.attrs['onchange'] = 'crtoadFile(event)'

        self.fields['PresentLocationDivision'].widget.attrs['onchange'] = 'FPrLDivi(this)'
        self.fields['PresentLocationDistrict'].widget.attrs['onchange'] = 'FPrLDist(this)'

        self.fields['PermanentLocationDivision'].widget.attrs['onchange'] = 'FPeLDivi(this)'
        self.fields['PermanentLocationDistrict'].widget.attrs['onchange'] = 'FPeLDist(this)'

        self.fields['PresentArea'].widget.attrs['style'] = 'width: 100%; font-size: 16px;'
        self.fields['PresentLocation'].widget.attrs['placeholder'] = 'E.g: Flat 3A, House 1410, Isha Kha Avenue, Sector 6, Uttara, Dhaka.'
        self.fields['PresentLocation'].widget.attrs['style'] = 'width: 100%; font-size: 16px;'
        self.fields['PermanentLocation'].widget.attrs['style'] = 'width: 100%; font-size: 16px;'
        self.fields['PermanentLocation'].widget.attrs['placeholder'] = 'Type your full address'
        self.fields['PreferredArea'].widget.attrs['style'] = 'width: 100%; font-size: 16px;'
        self.fields['Note'].widget.attrs['style'] = 'width: 100%; font-size: 16px;'
        self.fields['Note'].widget.attrs['placeholder'] = 'Anything that not included in our form or you want to mention'
        self.fields['CoachingCenterName'].widget.attrs['placeholder'] = 'Which coaching centers(If any)'
        self.fields['CoachingCenterName'].widget.attrs['style'] = 'width: 100%;'
        self.fields['AbroadUniversity'].widget.attrs['placeholder'] = 'Type your university name'
        self.fields['BirthDate'].widget.attrs['type'] = 'date'
        self.fields['IELTSPoint'].widget.attrs['placeholder'] = 'Detailed mark'
        self.fields['TOFELPoint'].widget.attrs['placeholder'] = 'Detailed mark'
        self.fields['GMATPoint'].widget.attrs['placeholder'] = 'Detailed mark'
        self.fields['GREPoint'].widget.attrs['placeholder'] = 'Detailed mark'
