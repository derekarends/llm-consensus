import logging

from typing import Annotated, List
from semantic_kernel.functions.kernel_function_decorator import kernel_function

logger = logging.getLogger(__name__)

class ExecutionPlugin:
    name = "ExectuionPlugin"

    @kernel_function(
        description="Makes an API call to a agent that is able to execute kubernetes commands."
    )
    def call_executor(
        self, question: Annotated[str, "The question used to determine what to execute"]
    ) -> Annotated[str, "Returns a string with the output of the command."]:
        logger.info(f"Calling executor with: {question}")
        return "Command executed"


class AggregatorPlugin:
    name = "AggregatorPlugin"

    @kernel_function(description="Makes an API call to a agent that is able to aggregate data.")
    def call_aggregator(
        self, question: Annotated[str, "The question to ask all involved llms"]
    ) -> Annotated[List[str], "The respnse for all llms, and the aggregated response."]:
        logger.info(f"Calling aggregator with: {question}")
        return ["response1", "response2", "response3", "aggregated response"]
