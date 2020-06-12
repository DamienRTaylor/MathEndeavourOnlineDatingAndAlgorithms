class Person:
    def __init__(self, QuestionsAnswered):
        #More information would be here such as name, age, gender and all that stuff
        self.QuestionsAnswered = [Question.ConvertListToQuestionClass(question) for question in QuestionsAnswered] #makes each question a question instance rather than a list

class Question:
    def __init__(self,Name,Answer,DesiredAnswer,ImportanceWeighting):
        self.Name = Name 
        self.Answer = Answer
        self.DesiredAnswer = DesiredAnswer
        self.ImportanceWeighting = ImportanceWeighting

    @staticmethod
    def ConvertListToQuestionClass(question):
        return Question(question[0],question[1].upper(),question[2].upper(),question[3])

class Matcher:
    def __init__(self,personOne,personTwo):
        self.personOne = personOne
        self.personTwo = personTwo
        self.commonQuestionsIndexes = self.findCommonQuestions()
        #!= means is not equivalent to 
        #the len function is built into python and gets the number of items in a list
        if len(self.commonQuestionsIndexes) != 0: #confirms that the two people have atleast one question in common
            personOneMatchPercent = self.calcPersonsMatchPercent(self.personOne)
            personTwoMatchPercent = self.calcPersonsMatchPercent(self.personTwo)
            self.overallMatchPercent = self.calcOverallMatchPercent(personOneMatchPercent,personTwoMatchPercent)
        else:
            self.overallMatchPercent =  0.0
            #if their is no data that the two users share answers to than the system has no clue about whether they would be attracted to eachother, so set it to 0%

    def findCommonQuestions(self):
        CommonQuestionIndexes = []
        for IndexOne,QuestionOne in enumerate(self.personOne.QuestionsAnswered):
            for IndexTwo,QuestionTwo in enumerate(self.personTwo.QuestionsAnswered):
                if QuestionOne.Name == QuestionTwo.Name:
                    CommonQuestionIndexes.append((IndexOne,IndexTwo))
        
        return CommonQuestionIndexes

    def calcPersonsMatchPercent(self,calculatingPerson):
        if calculatingPerson == self.personOne:
            calculatingPersonIndex = 0
            matchPerson = self.personTwo
            matchPersonIndex = 1

        elif calculatingPerson == self.personTwo:
            calculatingPersonIndex = 1
            matchPerson = self.personOne
            matchPersonIndex = 0

        else:
            raise ValueError("calculatingPerson Argument must be the person instance for either personOne or personTwo")
        
        totalPoints = 0
        scoredPoints = 0
        for indexes in self.commonQuestionsIndexes:
            if calculatingPerson.QuestionsAnswered[indexes[calculatingPersonIndex]].DesiredAnswer == matchPerson.QuestionsAnswered[indexes[matchPersonIndex]].Answer:
                scoredPoints+= calculatingPerson.QuestionsAnswered[indexes[calculatingPersonIndex]].ImportanceWeighting
            
            totalPoints+= calculatingPerson.QuestionsAnswered[indexes[calculatingPersonIndex]].ImportanceWeighting
        return (scoredPoints/totalPoints)*100

    def calcOverallMatchPercent(self,matchPercentOne,matchPercentTwo):
        numCommonQuestions = len(self.commonQuestionsIndexes)
        #this is the nth root of the two match percents multiplied
        #where n is the number of common questions
        #since python doesn't have an nth root operator, I'm instead doing to the power of 1/n which is the same thing
        return (matchPercentOne * matchPercentTwo) ** (1.0/numCommonQuestions)

#                               [Question Text, answer, desired answer, weighting]
personOneQuestionsAnswered = [["Do you Believe in God?","yes","yes",250],["Are you a tidy person?","yes","no",1]]
personOne = Person(personOneQuestionsAnswered)
                                 #dont Match                                              match                         not answered
personTwoQuestionsAnswered = [["Are you a tidy person?","yes","no",10],["Do you Believe in God?","yes","yes",50],["Do you like Scary Movies?","yes","yes",5]]
personTwo = Person(personTwoQuestionsAnswered)

matcher = Matcher(personOne,personTwo)
print(matcher.overallMatchPercent) 
#outputs 91.10506463487546 which is the correct value