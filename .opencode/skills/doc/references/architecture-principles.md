![MedHead Logo](../../../images/logo.png)
# Architecture Principles

Too guide the architectural effort, the consortium members have collaboratively
defined a set of architectural principles by domain. As with
any principles, these should be striven for in all project initiatives, 
all project initiatives should strive to meet them and justify any divergence.


# Summary of Principles

* A. Enterprise Architecture Principles
  * Principle A1: Primacy of Principles
  * Principle A2: Maximize Benefit to the Enterprise
  * Principle A3: Compliance With Law and Regulatory Statutes
  * Principle A4: Adherence With the Hippocratic Oath at all levels
* B. IT (System, Data, Solutions, Security, and Operations) Architecture Principles
  * Principle B1:  Business Continuity of Patient Critical Systems
  * Principle B2:  Clarity Through a Fine Grain Separation of Concerns
  * Principle B3: Continuous Integration and Delivery
  * Principle B4: Early Comprehensive and Appropriate Automated Tests
  * Principle B5: Shift-Left Security
  * Principle B6: Opening the Possibility of Extension Through Event-Driven Capabilities
* C. Architectural Methodology and Process Principles
  * Principle C1: Tailoring the TOGAF 9.2 ADM
  * Principle C2: A Centralized, Curated, Architecture Repository as the Source of Truth
  * Principle C3: The Use of Agreed Upon Open Standards to Ensure High Standards
  * Principle C4: Fostering a Learning Culture With Proof of Concepts, Prototypes, and Spikes
     1. Provide a hypothesis for every learning
     1. Isolate proofs of concepts from production data and systems
     1. Relax compliance but consider the consequence of doing so
     1. Basic engineering, delivery, and Testing principles are not to be relaxed for the solution architecture of proofs of concepts
     
# A. Enterprise Architecture Principles

## Principle A1: Primacy of Principles

**Statement:**

The principles stated here apply to all consortium members, who we will collectively refer to as the **enterprise**.

**Rationale:** 

The only way we can provide a consistent and measurable level of quality information to decision-makers is if all organizations abide by the principles.

**Implications:**

Without this principle, exclusions, favoritism, and inconsistency would rapidly undermine the management of and coherency
of architectural decisions.

Architecture initiatives will not begin until they are examined for compliance with the principles.
A conflict with a principle will be resolved by changing the framework of the initiative.

## Principle A2: Maximize Benefit to the Enterprise
 
**Statement**: 

Architecture and macro design decisions are made to provide maximum benefit to the enterprise as a whole in its efforts to maximize value to patients impacted by those decisions.

**Rationale:**

This principle embodies "service above self." Decisions made from an enterprise-wide perspective have greater long-term 
value than decisions made from any particular organizational perspective. Maximum return on investment requires architectural and design 
decisions to adhere to enterprise-wide drivers and priorities. No minority group will detract from the benefit of the whole. However, this principle will not preclude any minority group from getting its job done.

## Principle A3: Compliance With Law and Regulatory Statutes

**Statement:**

Enterprise systems, processes, and delivery must comply with all relevant laws, policies, and regulations.

**Rationale:**

Enterprise policy is to abide by laws, policies, and regulations. This will not preclude business process improvements that lead to changes in policies and regulations.

**Implications:**

The enterprise must be mindful of complying with laws, regulations, and external policies regarding the collection, retention, and management of data.
Education and access to the rules. Efficiency, need, and common sense are not the only drivers. Changes in the law and changes in regulations may drive changes in our processes or applications. 


## Principle A4: Adherence to the Hippocratic Oath at all Levels

**Statement:**

As an enterprise supporting patient care and the medical profession, all organizational
 decisions should adhere to the Hipocratic objective of 'first do no harm' care level all consortium members and their internal staff.

**Rationale:**

Enterprise policy is to abide by the principles of patient care and recognize that 
organizational decisions can impact patient lives.

**Implications:**

The enterprise at all levels must be mindful of making decisions
that are optimized towards providing value to the patient as well
as the member organizations. There are direct monetary and reputational
consequences that may follow if this principle results in patient harm, 
either intentionally or through neglect. 

# B. IT (System, Data, Solutions, Security and Operations) Architecture Principles


## Principle B1:  Business Continuity of Patient Critical Systems
 
**Statement**: 

Patient-care critical operations, as well as other supporting behavior, are to be maintained in spite of system interruptions.

**Rationale:**

As patient care is considered a priority, all critical systems
must be built to respect the principles of fault tolerance, such that priority 
is placed against the reliability of such systems throughout their design, deployment, 
feature development, and use. Medical, business, and technical partners throughout the enterprise must 
be provided with the capability to continue their business functions regardless of external events. 
Hardware failure, targeted attacks, natural disasters, and data corruption should not be allowed to
disrupt or stop enterprise activities.

**Implications:**

Dependency on shared system applications mandates that the risks of business interruption 
must be established in advance and managed. Management includes, but is not limited to:
* SRE principles which monitor and continuously measure against target
SLI's.
* Periodic reviews of system health and risks.
* Incremental testing for performance, vulnerability, and exposure for every increment of the technical platform.
* Designing mission-critical services to assure business function continuity through redundant or alternative capabilities.
* Recoverability, redundancy, and maintainability should be addressed at the time of design.
* Applications must be assessed for criticality and impact on the enterprise's mission to support patient care.
* Recovery plans should exist for all critical systems.

## Principle B2:  Clarity Through a Fine Grain Separation of Concerns

**Statement:**

Systems, data, and information architecture, should avoid artificially conflating disparate responsibilities
into monolithic or centralized designs and resulting implementations.

**Rationale:**

Through natural entropy, complex architectures tend to evolve over time into intricate and hard-to-define webs of dependencies 
and misplaced responsibility. Components in such an architecture are often 
 tightly coupled at a high level. 
 
This can, over time, result in architectural debt, which constraints a platform's agility to respond to changing 
business or patient needs. Recognizing naturally-occurring, narrow, domain boundaries in different contexts, designs, and their 
resulting implementations can enable the creation of an overall architecture that 
provides transparency of different system capabilities as well any **intentional** dependencies between them.

**Implications:**

Architectural decisions should follow the principles and best practices of *domain-driven design* 
and *microservice architectures.* This involves an active partnership 
between technical and business teams in delivering capabilities to the organization
using a shared model and ubiquitous language, which reflects the domain of patient care.
Narrow responsibilities between technical capabilities should be identified and,
as far as possible, resemble metaphors for the problem domains being
addressed within the business-context in the real world. Technical solutions
should all be justified by and modeled based on their overall contribution to patient
care scenarios.

## Principle B3: Continuous Integration and Delivery

**Statement:**

Continuous integration and delivery of small and incremental changes are favored over 
slow feature cycle times and large integrations.

**Rationale:**

Continuous integration of small chunks and pipelines through to production reduces 
risk and provides early feedback of integration issues across large teams.
A fast and regular delivery cadence also encourages teams to reduce risk 
by the provision of more thorough testing and higher degrees.

**Implications:**

CI/CD pipelines should be easily (or automatically) triggered by appropriate 
change events on the state of the code repository responsible for storing source
code. To facilitate this, the following is also required:
* **Features should be clearly trackable in version control** using appropriate branching
or tagging techniques.
* **CI/CD** runs should be traceable to a given feature delivery.
* **CI/CD** runs generate clear logs or output, which may be analyzed to isolate 
failed builds or other builds, tests, and deliver steps.

## Principle B4: Early, Comprehensive, and Appropriate Automated Tests

**Statement:**

Applications should be built with the guidance of automated tests, which provide 
confidence in both the functional and non-functional correctness
of the implementation. 

**Rationale:**

Software bugs are inevitable and can be caused by both errors of code or understanding.
Early focus on testing ensures that software is 
built to specification and that the specification is validated before 
an investment is put into building the wrong solutions.

**Implication:**

This principle encourages the use of techniques from the family of test-first or test-driven development methods. 
In order to validate requirements early, it is recommended to utilize language from 
the business domain in tests.
 
Early requirements should be written in a form that facilitates testing.
 

**Implications:**
Teams should be advised to follow the testing pyramid and implement an appropriate 
level of testing at each of the following levels:
* Unit
* Integration
* End-to-end

Where services are inter-dependent, it is also advised to consider consumer contract
testing.

 
## Principle B5: Shift-Left Security

**Statement:** 

The overall platform security risk is reduced by specifying and adhering to security requirements 
from the very start of each work increment. 


**Rationale:**
Omitting security concerns when designing and implementing solution has been 
demonstrated to often result in a higher cost and risk to the business
as such concerns are picked up in late testing. Security concerns not identified 
in such scenarios present a higher risk to the business if they go undetected or 
present as exploited or identified vulnerabilities.

**Implications:**
By considering per-increment security requirements with every platform and software iteration, 
this risk is offset and can translate into a culture of security-first thinking, which
reduces the risk of breaking regulatory agreements, as well as the trust of patients and medical practitioners.

The following practices should be considered and adapted to enable a culture of shift-left security:

* Using the currently limited security resources of the consortium (and industry at large) as
*enablers* to coach the organization in shift left-security.
* Using methods such as **threat modeling* to consider security related non-functional requirements, based on risk, 
 during early definition of stories and requirements.
* Continuous and automated security testing to reduce the risk caused
by a dependence on human error or omission.
* A culture of security awareness and championship fostered throughout the enterprise.

## Principle B6: Opening the Possibility of Extension Through Event-Driven Capabilities

**Statement:** 

All technical components should be designed to continuously publish 
business events for all operations, enabling event-driven business capabilities.

**Rationale:**
 
Systems initially designed with a single responsibility can overtime become an
extension point for new behavior, which is not always directly 
related to the original responsibility of the system. Such extensions
can both slow down the original system as well as conflate its 
responsibility and violate the principle of single responsibility.

**Implications:**

Event-driven architectures simplify the extension of existing systems 
with new capabilities that react to business events elsewhere in the
platform. This can also have performance benefits, allowing for
horizontal scaling of business event subscribers.
  
# C. Architectural Methodology and Process Principles
 
## Principle C1: Tailoring the TOGAF 9.2 ADM

**Statement**

The enterprise architecture will be shaped through customization and continuous improvement of an architecture framework 
tailored from TOGAF 9.2's ADM.

**Rationale:**

In order to provide a shared language and understanding of architecture, it is 
necessary to start from a well-defined and opinionated base. The OpenGroup's
TOGAF provides a framework which is centered around requirements management.

TOGAF includes governance and guidance that support specialization of a framework 
and methodology which can ensure the necessary levels or rigor when delivering 
functionality relating to patient safety, data privacy, overall information 
security, and desirable levels of correctness.  
 
**Implications:**

TOGAF's ADM includes governance and safeguards which are 
required to ensure an architecture capable of meeting ethical, business,
and state-level requirements around patient-centric software.

The consortium's enterprise architecture function will be responsible
for partnering with medical, business, and technical stakeholders 
to agree on an architectural framework, which may also be modified
across projects and different business contexts.

## Principle C2: A Centralized, Curated, Architecture Repository as the Source of Truth

**Statement:**
All architecturally-relevant information should be made available 
by a central architecture repository, which is continuously curated
by, and under the custodianship of, the enterprise architecture function.

**Rationale:**

Where architecture artifacts are dispersed across multiple systems, it becomes
difficult, over time, for all partners to have a clear oversight of 
the current *relevant* state of the architecture and agreed-upon architectural 
framework and processes.

**Implications:**

A centralized architecture repository simplifies the problem of 
consolidating and curating all current architecture-level artifacts, decisions, and 
content in a landscape of constantly changing business and technical requirements.

## Principle C3: The Use of Agreed-Upon Open Standards to Ensure High Standards

**Statement:**

Applying agreed-upon open standards and best practices can support the organization by providing the benefit of industry
learnings and expertise. 

**Rationale:** 

The principles outlined here build on industry best practices that have evolved alongside
supporting standards and guidelines. Using associated standards can support the benefits 
of the principles we align with.

**Implications:**

We will encourage and support, at least, the following open standards and best practice architectural patterns. All 
designs and architectures should be designed, where appropriate, to support extensions. 

**Initiatives are advised to document how their solutions either support these standards or are designed to be extended to support them.**  

* Event-driven architectures
  * Event sourcing
* Microservices architectures
  * OpenAPI specification of service contracts
  * Service meshes
     * Service observability
     * Service monitoring
     * Service discovery
     * Service integration visibility
  * Deployment through containerized, immutable, and repeatable infrastructure
* Domain-driven design
* Behavior-driven development
  * To ensure the correctness of expected patient-centric outcomes.
  * To support an aligning development with a ubiquitous language.
* Fault tolerance and design for long-term chaos engineering.
* OpenID Connect integration with state-run patient identity providers.
* Technology selection:
  * Should favor JVM languages due to consortium guidelines.  
* Documentation:
  * Should favor Javadoc or NDoc for source code and markdown or ASCIIdoc for project-level documentation.

As this defines a target state, it is acceptable to compromise on these, but such compromises should be documented and justified. 

## Principle C4: Fostering a Learning Culture With Proof of Concepts, Prototypes, and Spikes

**Statement:**
 
The enterprise encourages learning-centric implementations that reduce risk, validate assumptions, and 
invest in the learning required to evolve the platform responsibly.

**Rationale:**
The consortium collectively encourages the use of proof of concepts, spikes, and prototypes, as well as 
other investigative avenues of pursuit in order to *safely fail-fast* around
areas where there is insufficient information available to understand the risk of making 
 specific production-level design or implementation decisions. 
 
The cost of investing in learning efforts to reduce risk is encouraged across the 
enterprise as a means of protecting the interests of patients, partners, and the enterprise.

**Implications:**

The consortium partners collectively agree to stimulate a culture
 of evidence-based, and learning-centric, decision making. 
 
In so doing, the following exceptions and considerations should apply:

**i) Provide a hypothesis for every learning**

* All learning related implementations should be accompanied with a *hypothesis* defining the 
desired learning and how to measure whether that learning outcome has been achieved.


**ii) Isolate proofs of concepts from production data and systems**

* Action should be taken to mitigate or eliminate the risk of impacting patients where there is risk or uncertainty of
causing harm to the patient or enterprise. For example, learning may be conducted in isolation within a contrived environment to avoid impacting production systems.

**Use fabricated or anonymized data** 

* Patient data should be protected from high-risk learning activities which 
may impact data security or patient care. Early proof of concepts 
may use anonymized or fabricated data where possible.

**iii) Relax compliance but consider the consequence of doing so**

* Governance standards and levels of compliance may be 
relaxed where steps are taken to protect production systems and patient data. For example, proof of concepts
isolated from real patient data and production systems are not required to
conform to external standards or all enterprise governance around its ability to be released. 
* Where standards and governance are not fully adhered to, 
implementers and designers should recognize the need to 
consider how such prototypes or learning-focused implementations 
may feed their lessons into final producible implementations.
* It is strongly discouraged to produce prototypes directly, but 
 instead ensure that designs account for the side-effects of 
 the production that may invalidate any leanings. Eg., Omitting security concerns
 or expected data-volume may result in performance penalties which 
 invalidate learnings from an unscalable prototype. 
* Performance testing of prototypes and learning-centric implementations 
should demonstrate the key algorithms that form part of that learning scale.


**iv) Basic engineering, delivery, and testing principles are not to be relaxed for the solution architecture of proofs of concepts**

Proof of concepts should specifically aim to adhere to the following principles:
* Principle B1: Business continuity of patient critical systems
* Principle B2: Clarity through a Fine Grain Separation of Concerns
* Principle B3: Continuous Integration and Delivery
* Principle B4: Early Comprehensive and Appropriate Automated Tests

**v) Test plans as a tool for communicating requirements**
* Deliverables with self-documented test plans are preferred over externally documented test plans.
* Proof of concepts should have test plans describing how the product should behave.
* Test plans should utilize BDD (See C3) to describe business acceptance criteria that are in scope.
* Test plans should use the shared language of the business and be understandable by 
 technical and non-technical partners. 

**vi) Test execution reports as documentation for supported behavior**

To support the visibility of supported behavior, continuous learning, and transparency around software state: 
* PoCs should have CI pipelines that run tests and produce test execution reports.
* CI environments should allow software owners to inspect past runs and degradations of the build*, which may affect any learnings from the hypothesis in Line with B3.