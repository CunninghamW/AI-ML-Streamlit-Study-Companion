class ProgressTracker:
    
    def __init__(self):
        self.questions_answered = {}
        self.category_stats = {}
        self.overall_stats = {}
        self.total_answered = 0
        self.total_correct = 0
        self.weak_categories = {}
        
        

    def update_progress(self, question_id, category, correct: bool):
        
        # prevent double counting
        if question_id in self.questions_answered:
            return   # ignore repeated attempts

        # record answer
        self.questions_answered[question_id] = correct

        # update totals
        self.total_answered += 1
        if correct:
            self.total_correct += 1
                    
        
        # update the user overall accuracy
        self.overall_accuracy = (self.total_correct / self.total_answered) * 100

        # update the overall stats
        self.overall_stats["total_answered"] = self.total_answered
        self.overall_stats["total_correct"] = self.total_correct
        self.overall_stats["overall_accuracy"] = self.overall_accuracy


        # call _update_category_stats method to seamlesslly update category stats
        self._update_category_stats(category, correct)

        

        
    def _update_category_stats(self, category, correct: bool):
        
        # check if category in the category_stats dict, if not initalize it
        if category not in self.category_stats:
            self.category_stats[category] = {"correct": 0, "total": 0, "accuracy": 0}
        
        # increment the "total" key in category_stats
        self.category_stats[category]["total"] += 1
        
        # increment the "correct" key if correct
        if correct == True:
            self.category_stats[category]["correct"] += 1
        
        # update the accuracy of teh categories
        self.category_stats[category]["accuracy"] = (self.category_stats[category]["correct"] / self.category_stats[category]["total"]) * 100

        # if weak in a category add to weak_categories dict
        accuracy = self.category_stats[category]["accuracy"]
        if accuracy < 50:
            self.weak_categories[category] = self.category_stats[category]["accuracy"]

        # if accuracy improves on a weak category, remove it from weak_categories
        else:
            self.weak_categories.pop(category, None)


    def get_summary(self):
        return {
            "overall": self.overall_stats,
            "categories": self.category_stats,
            "weak_categories": self.weak_categories
        }

    def reset_progress(self):
        self.total_answered = 0
        self.total_correct = 0
        self.overall_accuracy = 0
        self.overall_stats = {}
        self.category_stats = {}
        self.weak_categories = {}
        self.questions_answered = {}
