from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Submission, Question, Choice

def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        selected_ids = []
        score = 0

        for question in course.questions.all():
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                selected_ids.append(int(selected_choice_id))
                
                choice = Choice.objects.get(id=selected_choice_id)
                if choice.is_correct:
                    score += 1

        submission = Submission.objects.create(
            course=course,
            score=score,
        )

        request.session['selected_ids'] = selected_ids
        request.session['score'] = score
        request.session['submission_id'] = submission.id

        return redirect('show_exam_result', course_id=course.id, submission_id=submission.id)

    return redirect('course_detail', course_id=course.id)


def show_exam_result(request, course_id, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    selected_ids = request.session.get('selected_ids', [])
    score = request.session.get('score', 0)

    possible = submission.course.questions.count()

    return render(request, 'result.html', {
        'selected_ids': selected_ids,
        'grade': score,
        'possible': possible,
    })
