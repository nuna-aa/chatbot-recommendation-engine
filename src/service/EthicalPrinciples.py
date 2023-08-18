from langchain.chains import ConstitutionalChain
from langchain.chains.constitutional_ai.models import ConstitutionalPrinciple


class EthicalPrinciples:
    
    __non_pharmacological_principle = ConstitutionalPrinciple(
        name='Non pharmacological Principle',
        critique_request="Identify specific ways in which the model's response is recommending drugs, medicines, any pharmacological treatment.",
        revision_request="Please rewrite the model response to remove all content that includes pharmacological treatment. The model response should only include non-pharmacological and mon-medical content.",
    )
    __only_osteoporosis_content = ConstitutionalPrinciple(
        name='Only Osteoporosis Content',
        critique_request="Identify specific ways in which the model's response contains content that does not relate to Osteoporosis, physical activities, exercies, diet adjustments or stress management techniques",
        revision_request="Please rewrite the model response to remove all content that does not pertain to Osteoporosis, physical activities, exercies, diet adjustments or stress management techniques",
    )
    
    #__ethical_principles = ConstitutionalChain.get_principles(["uo-utility-7", "uo-implications-2", "uo-ethics-1",
    #                                                         "uo-ethics-2", "uo-security-2", "criminal",
    #                                                         "age-innappropriate", "harmful5"])

    __ethical_principles = ConstitutionalChain.get_principles(["uo-implications-2", "harmful1"])

    context_principles: list[ConstitutionalPrinciple] = [__only_osteoporosis_content, __non_pharmacological_principle]

    context_principles.extend(__ethical_principles)
    
    