from django.db import models

from .abstracttable import AbstractTable
from .paper_setup_description import PaperSetupDescription
from .passage_instruction_contents import PassageInstructionContents


class PaperSetupPassageMap(AbstractTable):
    paper_setup_id = models.ForeignKey(PaperSetupDescription, on_delete= models.CASCADE)
    passage = models.ForeignKey(PassageInstructionContents,on_delete=models.CASCADE, null= True, blank= True)
    

    class Meta:
        db_table = "paper_setup_passage_map"

    def __str__(self):
        return f'{self.paper_setup_id} {self.passage}'
