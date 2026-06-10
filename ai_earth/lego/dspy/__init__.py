"""
DSPy — Compiling Declarative Language Model Calls into Self-Improving Pipelines
================================================================================
Source: https://github.com/stanfordnlp/dspy (28K ⭐, ICLR 2024)
Extracted as LEGO piece for AI Earth — verbatim source files, lazy init.

NOTE: This __init__.py uses lazy imports to avoid circular dependencies
that exist in the original codebase. All actual source files are VERBATIM.
"""

# Version
try:
    from dspy.__metadata__ import __version__
except ImportError:
    __version__ = "3.0.0"

# ══════════════════════════════════════════════════════════════════════
# Level 0: Foundation (no dspy deps)
# ══════════════════════════════════════════════════════════════════════
from dspy.utils.constants import IS_TYPE_UNDEFINED
from dspy.utils.exceptions import (
    AdapterParseError,
    ContextWindowExceededError,
    DSPyError,
    LMAuthError,
    LMBillingError,
    LMConfigurationError,
    LMError,
    LMInvalidRequestError,
    LMNotConfiguredError,
    LMProviderError,
    LMRateLimitError,
    LMServerError,
    LMTimeoutError,
    LMTransportError,
    LMUnexpectedError,
    LMUnsupportedFeatureError,
    LMUnsupportedModelError,
    is_retryable_lm_error,
)
from dspy.utils.logging_utils import configure_dspy_loggers, disable_logging, enable_logging
from dspy.utils.asyncify import asyncify
from dspy.utils.syncify import syncify
from dspy.utils.saving import load
from dspy.utils.usage_tracker import track_usage

# ══════════════════════════════════════════════════════════════════════
# Level 1: Primitives (depend on foundation)
# ══════════════════════════════════════════════════════════════════════
from dspy.primitives.example import Example
from dspy.primitives.prediction import Completions, Prediction
from dspy.primitives.base_module import BaseModule
from dspy.primitives.sandbox_serializable import SandboxSerializable

# ══════════════════════════════════════════════════════════════════════
# Level 2: Settings + Core Types
# ══════════════════════════════════════════════════════════════════════
from dspy.dsp.utils.settings import settings

try:
    from dspy.core import (
        Assistant,
        Developer,
        LMConfig,
        LMMessage,
        LMRequest,
        LMResponse,
        System,
        ToolCall,
        ToolResult,
        User,
    )
except ImportError:
    pass

# ══════════════════════════════════════════════════════════════════════
# Level 3: Signatures (depend on primitives)
# ══════════════════════════════════════════════════════════════════════
from dspy.signatures.field import InputField, OutputField
from dspy.signatures.signature import Signature, ensure_signature

# ══════════════════════════════════════════════════════════════════════
# Level 4: Module (depends on signatures + parallel)
# ══════════════════════════════════════════════════════════════════════
from dspy.primitives.module import Module

# ══════════════════════════════════════════════════════════════════════
# Level 5: Adapters (depend on signatures + types)
# ══════════════════════════════════════════════════════════════════════
try:
    from dspy.adapters import Adapter, ChatAdapter, JSONAdapter, XMLAdapter, TwoStepAdapter
    from dspy.adapters.types import Image, Audio, File, History, Type, Tool, ToolCalls, ToolCallResults, Code, Reasoning
except ImportError:
    pass

# ══════════════════════════════════════════════════════════════════════
# Level 6: Predictors (depend on module + adapters + clients)
# ══════════════════════════════════════════════════════════════════════
try:
    from dspy.predict.predict import Predict
    from dspy.predict.chain_of_thought import ChainOfThought
    from dspy.predict.program_of_thought import ProgramOfThought
    from dspy.predict.refine import Refine
    from dspy.predict.retry import Retry
    from dspy.predict.best_of_n import BestOfN
    from dspy.predict.parallel import Parallel
    from dspy.predict.multi_chain_comparison import MultiChainComparison
    from dspy.predict.aggregation import majority
    from dspy.predict.knn import KNN
    from dspy.predict.code_act import CodeAct
    from dspy.predict.react import ReAct, Tool as PredictTool
except ImportError:
    pass

# ══════════════════════════════════════════════════════════════════════
# Level 7: Evaluate (depends on predict)
# ══════════════════════════════════════════════════════════════════════
try:
    from dspy.evaluate.evaluate import Evaluate
    from dspy.evaluate.metrics import answer_exact_match, answer_passage_match, normalize_text
except ImportError:
    pass

# ══════════════════════════════════════════════════════════════════════
# Level 8: Clients (LM abstraction)
# ══════════════════════════════════════════════════════════════════════
try:
    from dspy.clients.lm import LM
    from dspy.clients.base_lm import BaseLM
    from dspy.clients.provider import Provider
    from dspy.clients.embedding import Embedder
except ImportError:
    pass

# ══════════════════════════════════════════════════════════════════════
# Level 9: Teleprompters (optimizers — depends on everything)
# ══════════════════════════════════════════════════════════════════════
try:
    from dspy.teleprompt.teleprompt import Teleprompter
    from dspy.teleprompt.vanilla import LabeledFewShot
    from dspy.teleprompt.bootstrap import BootstrapFewShot
    from dspy.teleprompt.mipro_optimizer_v2 import MIPROv2
    from dspy.teleprompt.copro_optimizer import COPRO
    from dspy.teleprompt.ensemble import Ensemble
    from dspy.teleprompt.random_search import BootstrapFewShotWithRandomSearch
    from dspy.teleprompt.simba import SIMBA
    from dspy.teleprompt.bettertogether import BetterTogether
    from dspy.teleprompt.bootstrap_finetune import BootstrapFinetune
    from dspy.teleprompt.bootstrap_trace import bootstrap_trace_data
    from dspy.teleprompt.infer_rules import InferRules
    from dspy.teleprompt.knn_fewshot import KNNFewShot
except ImportError:
    pass

try:
    from dspy.teleprompt.teleprompt_optuna import BootstrapFewShotWithOptuna
except ImportError:
    pass

try:
    from dspy.teleprompt.gepa.gepa import GEPA
except ImportError:
    pass

# ══════════════════════════════════════════════════════════════════════
# Level 10: Streaming (optional)
# ══════════════════════════════════════════════════════════════════════
try:
    from dspy.streaming.streamify import streamify
except ImportError:
    pass

# ══════════════════════════════════════════════════════════════════════
# Propose (for MIPROv2)
# ══════════════════════════════════════════════════════════════════════
try:
    from dspy.propose import GroundedProposer
except ImportError:
    pass
