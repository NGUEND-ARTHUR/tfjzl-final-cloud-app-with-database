from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson, Question, Choice, Submission


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, "course_details_bootstrap.html", {"course": course})


def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        score = 0
        total = 0

        for lesson in course.lessons.all():
            for question in lesson.questions.all():
                total += 1
                choice_id = request.POST.get(f"question_{question.id}")

                if choice_id:
                    choice = Choice.objects.get(id=choice_id)

                    Submission.objects.create(
                        question=question,
                        selected_choice=choice
                    )

                    if choice.is_correct:
                        score += 1

        request.session['score'] = score
        request.session['total'] = total

        return redirect('show_exam_result')

    return redirect('course_detail', course_id=course.id)


def show_exam_result(request):
    score = request.session.get('score', 0)
    total = request.session.get('total', 0)

    return render(request, "result.html", {
        "score": score,
        "total": total
    })
