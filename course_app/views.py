from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Submission, Question, Choice

# ✅ 1. Dashboard / Course List (WITH AUTH)
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {
        'courses': courses
    })


# ✅ 2. Course Detail Page (WITH AUTH)
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(request, 'course_detail.html', {
        'course': course
    })


# ✅ 3. Submit Exam
@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        selected_ids = []
        score = 0

        # 🔥 FIX: Access questions correctly via lessons
        questions = Question.objects.filter(lesson__course=course)

        for question in questions:
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

        return redirect('show_exam_result', course_id=course.id, submission_id=submission.id)

    return redirect('course_detail', course_id=course.id)


# ✅ 4. Show Result
@login_required
def show_exam_result(request, course_id, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    selected_ids = request.session.get('selected_ids', [])
    score = request.session.get('score', 0)

    possible = Question.objects.filter(lesson__course=submission.course).count()

    return render(request, 'result.html', {
        'selected_ids': selected_ids,
        'grade': score,
        'possible': possible,
    })
