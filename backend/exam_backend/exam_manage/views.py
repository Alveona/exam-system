from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from .models import Question, Answer, Course, UserCourseRelation, StrictMode, Hint, QuestionMedia
from .serializers import QuestionSerializer, AnswerSerializer, CourseSerializer, \
    QuestionListSerializer, CourseCreatedSerializer, RelationSerializer, RelationUnsubscribeSerializer, \
    AnswerFormDataSerializer, StrictModeSerializer, QuestionMediaSerializer, HintSerializer

class QuestionListViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Question.objects.all()
            return queryset
        return Question.objects.all().filter(user=user)



class AnswerFormDataViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerFormDataSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', 'patch', 'get']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Answer.objects.all().filter(question=self.request.query_params.get('id'),
                                                   question__user=self.request.user, deleted = False)
            print(queryset)
            return queryset
        # if self.request.method == "DELETE": # what was going on here?
            # print('object deleted')
        user = self.request.user
        if user.is_superuser:
            queryset = Answer.objects.all().filter(deleted = False)
            return queryset
        return Answer.objects.all().filter(question__user=user, deleted = False)

    # def create(self, request, *args, **kwargs):
    #     # here we parse all answers came after the question
    #     # we use form-data as there are files to upload
    #     # TODO: look at https://www.django-rest-framework.org/api-guide/parsers/#formparser
    #     print(self.request.data)
    #     print(self.request.POST.getlist('image'))
    #     print(self.request.POST.get('image'))
    #     _dict = dict(self.request.data)
    #     print(_dict)
    #     question_to_parse = []
    #     text_to_parse = []
    #     correct_to_parse = []
    #     weight_to_parse = []
    #     audio_to_parse = []
    #     hint_to_parse = []
    #     priority_to_parse = []
    #     image_to_parse = []
    #     for value in _dict['question']:
    #         question_to_parse.append(value)
    #     for value in _dict['text']:
    #         text_to_parse.append(value)
    #     for value in _dict['correct']:
    #         correct_to_parse.append(value.capitalize())
    #     for value in _dict['weight']:
    #         weight_to_parse.append(value)
    #     # for value in _dict['audio']:
    #     #     audio_to_parse.append(value if value != 'null' else None)
    #     # print(audio_to_parse)
    #     # for value in _dict['hint']:
    #     #     hint_to_parse.append(value if value != 'null' else None)
    #     for value in _dict['image']:
    #         image_to_parse.append(value if value != 'null' else None)
    #     for value in _dict['priority']:
    #         priority_to_parse.append(value)
    #     print('len: ' + str(len(question_to_parse)))
    #
    #     successfully_created_answers = [] # used to easily revert all creates if exception occured
    #     #try:
    #     ids_arr = []
    #     for i in range(0, len(question_to_parse)):
    #         question = Question.objects.all().get(id=question_to_parse[i])
    #         answer = Answer(question=question, text=text_to_parse[i],
    #                         correct=correct_to_parse[i], weight=weight_to_parse[i],
    #                         priority=priority_to_parse[i], image=image_to_parse[i], deleted = False)
    #         answer.save()
    #         # hint = Hint(answer = answer, )
    #         successfully_created_answers.append(answer)
    #         print('id:' + str(answer.id))
    #         ids_arr.append(answer.id)
    #     return Response({"answers" : ids_arr})
    #     # except:
    #     #     # yup, we don't set 'deleted' to them, but directly delete from database because
    #     #     # something went completely wrong so we don't need partically written answers
    #     #     print('Unable to create object, clearing all them up')
    #     #     for ans in successfully_created_answers:
    #     #         ans.delete()
    #     #     return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        validated_data = self.request.data
        question = Question.objects.all().get(id=validated_data['question'])
        answer = Answer(question=question, text=validated_data['text'],
                        correct=validated_data['correct'].capitalize(), weight=validated_data['weight'],
                        priority=validated_data['priority'], deleted = False)
        if validated_data['image'] != 'null':
             answer.image=validated_data['image']
        answer.save()
        return Response({'answer' : answer.id}, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        validated_data = self.request.data
        print(validated_data)
        answer = self.get_object()
        if 'text' in validated_data:
            answer.text = validated_data['text']
        if 'image' in validated_data:
            # print(validated_data['image'])
            if validated_data['image'] == 'null':
                answer.image = ''
            else:
                if validated_data['image'] != 'stay':
                    answer.image = validated_data['image']
        if 'correct' in validated_data:
            # if validated_data['correct'] == 'true':
            #     answer.correct = True
            # if validated_data['correct'] == 'false':
            #     answer.correct = tru
            answer.correct = (validated_data['correct']).capitalize()
        if 'weight' in validated_data:
            answer.weight = validated_data['weight']
        if 'priority' in validated_data:
            answer.priority = validated_data['priority']
        answer.save()
        return Response({'answer' : answer.id}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()

    serializer_class = QuestionSerializer
    # serializer = QuestionSerializer()
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete', 'patch']
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        validated_data = self.request.data
        print(validated_data)
        question = Question(user=self.request.user, title=validated_data['title'],
                            text=validated_data['text'], answer_type=validated_data['answer_type'])
        # if 'timer' in validated_data:
        #     question.timer = validated_data['timer']
        if 'attempts_number' in self.request.data:
            print(self.request.data['attempts_number'])
            if self.request.data['attempts_number'] != 'null':
                print('if')
                question.attempts_number = self.request.data['attempts_number']
            else:
                print('else')
                # question.attempts_number = None
        if 'answers_number' in validated_data:
            question.answers_number = validated_data['answers_number']
        if 'difficulty' in validated_data:
            question.difficulty = validated_data['difficulty']
        if 'comment' in validated_data:
            question.comment = validated_data['comment']

        question.save()
        return Response({"id" : question.id})


    def get_queryset(self):
        user = self.request.user
        if self.request.method == "GET":
            queryset = Question.objects.all().filter(id=self.request.query_params.get('id'),
                                                     user=user)
            print(queryset)
            return queryset
        if user.is_superuser: # TODO: either do this for all get's or delete it from here, no more methods support this logic
            queryset = Question.objects.all()
            return queryset
        return Question.objects.all().filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.method == "DELETE":
            print('del')
            # if it is delete request, then mark answer as 'deleted' and delete only question
            answers = Answer.objects.all().filter(question=instance.id)
            for ans in answers:
                ans.deleted = True
                ans.save()
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            Answer.objects.all().filter(question=instance.id).delete()
        # otherwise delete question with constraints
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        validated_data = self.request.data
        question = self.get_object()
        print(validated_data)
        # answers = Answer.objects.all().filter(question = question)
        # answers.delete() # we assume that there will be new answers after question

        question.title = validated_data['title']
        question.text = validated_data['text']
        question.answer_type = validated_data['answer_type']
        # question = Question(user=self.context['request'].user, title=validated_data['title'],
        #                     text=validated_data['text'], answer_type=validated_data['answer_type'])
        # if 'timer' in validated_data:
        #     question.timer = validated_data['timer']
        try:
            if 'attempts_number' in validated_data:
                if validated_data['attempts_number'] != 'null':
                    question.attempts_number = validated_data['attempts_number']
                else:
                    question.attempts_number = None
        except:
            # else:
            question.attempts_number = None
        if 'answers_number' in validated_data:
            question.answers_number = validated_data['answers_number']
        if 'difficulty' in validated_data:
            question.difficulty = validated_data['difficulty']
        if 'comment' in validated_data:
            question.comment = validated_data['comment']
        # print(self.request.data)
        if 'image' in validated_data:
            # print(validated_data['image'])
            if validated_data['image'] == 'null':
                question.image = ''
            else:
                if validated_data['image'] != 'stay':
                    question.image = validated_data['image']
        if 'audio' in validated_data:
            # print(validated_data['audio'])
            if validated_data['audio'] == 'null':
                question.audio = ''
            else:
                if validated_data['audio'] != 'stay':
                    question.audio = validated_data['audio']
        question.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()






class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete', 'patch']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Answer.objects.all().filter(question=self.request.query_params.get('id'),
                                                   question__user=self.request.user, deleted = False)
            print(queryset)
            return queryset
        # if self.request.method == "DELETE":
            # print('object deleted')
        user = self.request.user
        if user.is_superuser:
            queryset = Answer.objects.all().filter(deleted = False)
            return queryset
        return Answer.objects.all().filter(question__user=user, deleted = False)

    def create(self, request, *args, **kwargs):
        print(self.request.data)
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    lookup_field = 'token' # used to allow delete on /api/courses/<token>/
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        validated_data = self.request.data
        print(validated_data)
        questions_to_parse = request.POST.getlist('questions')
        # https://stackoverflow.com/questions/12101658/how-to-get-an-array-in-django-posted-via-ajax
        print(questions_to_parse)
        course = Course(name=validated_data['name'], description=validated_data['description'],
                        questions_number=validated_data['questions_number'],
                        token=validated_data['token'],

                        author=validated_data['author'])
        course.perfect_mark = self.request.data['perfect_mark']
        course.good_mark = self.request.data['good_mark']
        course.satisfactory_mark = self.request.data['satisfactory_mark']
        if 'perfect_audio' in self.request.data:
            if self.request.data['perfect_audio'] != 'null':
                course.perfect_audio = self.request.data['perfect_audio']
            else:
                course.perfect_audio = None
        if 'good_audio' in self.request.data:
            if self.request.data['good_audio'] != 'null':
                course.good_audio = self.request.data['good_audio']
            else:
                course.good_audio = None
        if 'satisfactory_audio' in self.request.data:
            if self.request.data['satisfactory_audio'] != 'null':
                course.satisfactory_audio = self.request.data['satisfactory_audio']
            else:
                course.satisfactory_audio = None

        if 'video' in self.request.data:
            if self.request.data['video'] != 'null':
                course.video = self.request.data['video']
            else:
                course.video = ''
        if 'attempts' in validated_data and self.request.data['attempts'] != '':
            course.attempts = self.request.data['attempts']
        course.save()
        #questions = self.context['request'].data['questions']
        #questions_to_parse = validated_data['questions']

        if questions_to_parse:
            for question in questions_to_parse:
                course.questions.add(question)

        if 'image' in validated_data:
            course.image = validated_data['image']

        if 'user' in validated_data:
            user = validated_data['user']
        else:
            user = self.request.user


        user_relation = UserCourseRelation(user=user, course=course, access=1)
        user_relation.save()
        course.save()
        # return course
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Course.objects.all().filter(token=self.request.query_params.get('token'))
            return queryset
        return Course.objects.all()

    def destroy(self, request, *args, **kwargs):
        # if self.request.method == "DELETE":
        instance = self.get_object()
        UserCourseRelation.objects.all().filter(course=instance).delete()
        CourseSession.objects.all().filter(course=instance).delete()
        Course.objects.all().get(token=instance.token).delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        validated_data = self.request.data
        course = self.get_object()
        if 'name' in validated_data:
            course.name = validated_data['name']
        if 'description' in validated_data:
            course.description = validated_data['description']
        if 'author' in validated_data:
            course.author = validated_data['author']
        if 'image' in validated_data:
            # print(validated_data['image'])
            if validated_data['image'] == 'null':
                course.image = ''
            else:
                if validated_data['image'] != 'stay':
                    course.image = validated_data['image']
        if 'questions_number' in validated_data:
            course.questions_number = validated_data['questions_number']
        if 'attempts' in validated_data:
            course.attempts = validated_data['attempts']
        if 'perfect_mark' in validated_data:
            course.perfect_mark = validated_data['perfect_mark']
        if 'good_mark' in validated_data:
            course.good_mark = validated_data['good_mark']
        if 'satisfactory_mark' in validated_data:
            course.satisfactory_mark = validated_data['satisfactory_mark']
        questions_to_parse = validated_data['questions']
        print(questions_to_parse)
        print(course.questions)
        course.questions.clear()
        print(course.questions)
        if questions_to_parse:
            for question in questions_to_parse:
                course.questions.add(question)

        course.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class CourseCreatedViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseCreatedSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Course.objects.all().filter(user=self.request.user).distinct()
            # print(queryset)
            if not queryset:
                return queryset
            for course in queryset:
                queryset_access = UserCourseRelation.objects.all().filter(course=course,
                                                                          user=self.request.user, access=1)
                # print(queryset_access)
                if not queryset_access:
                    queryset = queryset.exclude(id=course.id)
            return queryset


class CourseAddedViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseCreatedSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Course.objects.all().filter(user=self.request.user).distinct()
            # print(queryset)
            ids = []
            if not queryset:
                return queryset
            for course in queryset:
                queryset_access = UserCourseRelation.objects.all().filter(access=0, course=course,
                                                                          user=self.request.user)
                # print(queryset_access)
                if not queryset_access:
                    queryset = queryset.exclude(id=course.id)
            return queryset


class RelationViewSet(viewsets.ModelViewSet):
    queryset = UserCourseRelation.objects.all()
    serializer_class = RelationSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']

    # lookup_field = 'token'

    def get_queryset(self):
        return None


class RelationUnsubscribeViewSet(viewsets.ModelViewSet):
    queryset = UserCourseRelation.objects.all()
    serializer_class = RelationUnsubscribeSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        course = Course.objects.all().get(token=self.request.data['token'])
        relation = UserCourseRelation(user=self.request.user,
                                      course=course, access=0)
        relation.delete()
        return Response({'status': 'Successfully deleted'})

class StrictModeViewSet(viewsets.ModelViewSet):
    queryset = StrictMode.objects.all()
    serializer_class = StrictModeSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'delete', 'patch']
    # lookup_field = 'id'
    def get_queryset(self):
        user = self.request.user
        if self.request.method == "GET":
            if self.request.query_params.get('token'):
                usercourse = UserCourseRelation.objects.all().get(course__token = self.request.query_params.get('token'), \
                                                                  access = 1)
                queryset = StrictMode.objects.all().filter(user = usercourse.user)
            else:
                queryset = StrictMode.objects.all().filter(user = user)
            print(queryset)
            return queryset
        if user.is_superuser:
            queryset = StrictMode.objects.all()
            return queryset
        return StrictMode.objects.all().filter()

    def destroy(self, request, *args, **kwargs):
        print(self.request.data)
        print('delete')
        instance = self.get_object()
        print(instance)
        self.perform_destroy(instance)
        # instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
    # def perform_destroy(self, instance):
    #     instance.delete()

class QuestionMediaViewSet(viewsets.ModelViewSet):
    queryset = QuestionMedia.objects.all()
    serializer_class = QuestionMediaSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_queryset(self):
        user = self.request.user
        if self.request.method == "GET":
            queryset = QuestionMedia.objects.all().filter(question=self.request.query_params.get('question'))
            print(queryset)
            return queryset
        if user.is_superuser: # TODO: either do this for all get's or delete it from here, no more methods support this logic
            queryset = QuestionMedia.objects.all()
            return queryset
        return QuestionMedia.objects.all().filter()

    def create(self, request, *args, **kwargs):
        validated_data = self.request.data
        question = Question.objects.all().get(id = validated_data['question'])
        mode = StrictMode.objects.all().get(id = validated_data['mode'])
        media = QuestionMedia(question = question, mode = mode)
        if 'audio' in self.request.data:
            if self.request.data['audio'] == 'null':
                media.audio = None
            else:
                media.audio = self.request.data['audio']
        if 'video' in self.request.data:
            if self.request.data['video'] == 'null':
                media.video = None
            else:
                media.video = self.request.data['video']
        media.save()
        return Response(status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        validated_data = self.request.data
        question = Question.objects.all().get(id = validated_data['question'])
        mode = StrictMode.objects.all().get(id = validated_data['mode'])
        # media = QuestionMedia(question = question, mode = mode)
        media = self.get_object()
        if 'audio' in self.request.data:
            if self.request.data['audio'] == 'null':
                media.audio = ''
            else:
                if self.request.data['audio'] != 'stay':
                    # print('if')
                    media.audio = self.request.data['audio']
        if 'video' in self.request.data:
            if self.request.data['video'] == 'null':
                media.video = ''
            else:
                if self.request.data['video'] != 'stay':
                    media.video = self.request.data['video']
        media.save()
        return Response(status=status.HTTP_200_OK)

class HintViewSet(viewsets.ModelViewSet):
    queryset = Hint.objects.all()
    serializer_class = HintSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'delete', 'patch']
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if self.request.method == "GET":
            queryset = Hint.objects.all().filter(answer=self.request.query_params.get('answer'))
            print(queryset)
            return queryset
        if user.is_superuser: # TODO: either do this for all get's or delete it from here, no more methods support this logic
            queryset = Hint.objects.all()
            return queryset
        return Hint.objects.all().filter()

    def create(self, request, *args, **kwargs):
        validated_data = self.request.data
        answer = Answer.objects.all().get(id = validated_data['answer'])
        mode = StrictMode.objects.all().get(id = validated_data['mode'])
        hint = Hint(answer = answer, mode = mode)
        if 'audio' in self.request.data:
            if self.request.data['audio'] == 'null':
                hint.audio = None
            else:
                hint.audio = self.request.data['audio']
        if 'video' in self.request.data:
            if self.request.data['video'] == 'null':
                hint.video = None
            else:
                hint.video = self.request.data['video']
        if 'text' in self.request.data:
            hint.text = self.request.data['text']
        hint.save()
        return Response(status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        validated_data = self.request.data
        answer = Answer.objects.all().get(id = validated_data['answer'])
        mode = StrictMode.objects.all().get(id = validated_data['mode'])
        # hint = Hint(answer = answer, mode = mode)
        hint = self.get_object()
        if 'audio' in self.request.data:
            if self.request.data['audio'] == 'null':
                hint.audio = ''
            else:
                if self.request.data['audio'] != 'stay':
                    # print('if')
                    hint.audio = self.request.data['audio']
        if 'video' in self.request.data:
            if self.request.data['video'] == 'null':
                hint.video = ''
            else:
                if self.request.data['video'] != 'stay':
                    hint.video = self.request.data['video']
        if 'text' in self.request.data:
            hint.text = self.request.data['text']
        hint.save()
        return Response(status=status.HTTP_200_OK)
