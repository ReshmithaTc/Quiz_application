from django import forms
import json
import os

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        file_path = os.path.join(os.path.dirname(__file__), 'questions.json')
        with open(file_path, 'r') as f:
            questions = json.load(f)
        for q in questions:
            self.fields[f'question_{q["id"]}'] = forms.ChoiceField(
                label=q["question"],
                choices=[(option, option) for option in q["options"]],
                widget=forms.RadioSelect,
                required=True
            )
