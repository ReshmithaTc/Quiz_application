from django.shortcuts import render, redirect
from .forms import QuizForm
from django.contrib.auth.decorators import login_required
from .models import Result
from django.contrib.auth.forms import UserCreationForm

import json
import os

@login_required
def quiz_view(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        file_path = os.path.join(os.path.dirname(__file__), 'questions.json')
        with open(file_path, 'r') as f:
            questions = json.load(f)

        user_answers = {}
        correct_count = 0
        result_data = []

        if form.is_valid():
            for q in questions:
                qid = f'question_{q["id"]}'
                user_answer = form.cleaned_data.get(qid)
                is_correct = user_answer == q["answer"]
                if is_correct:
                    correct_count += 1
                result_data.append({
                    'question': q["question"],
                    'user_answer': user_answer,
                    'correct_answer': q["answer"],
                    'is_correct': is_correct
                })
            
            
            # Save result to database
            Result.objects.create(
                user=request.user,
                score=correct_count,
                total=len(questions)
            )
            

        return render(request, 'quiz/result.html', {
            'score': correct_count,
            'total': len(questions),
            'result_data': result_data
        })

    else:
        form = QuizForm()
    return render(request, 'quiz/quiz.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'quiz/signup.html', {'form': form})
