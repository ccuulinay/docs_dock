A well-crafted prompt is essential for instructing an AI to accurately analyze user-uploaded database metadata and generate meaningful descriptions for every possible value within each field. Here is a detailed guide and a template to help you write an effective prompt for this task.
Key Principles for an Effective Prompt
Before diving into the template, it's crucial to understand the principles of a good prompt for this specific use case:
 * Be Specific and Clear: The prompt should leave no room for ambiguity. Clearly state the objective: to get descriptions for each unique value in the database fields.
 * Provide Context: The AI needs to understand it is working with database metadata. Mentioning terms like "tables," "fields," "columns," and "values" will set the right context.
 * Define the Persona: Instruct the AI to act as a specific expert, such as a "Senior Data Analyst" or "Database Administrator." This helps in getting more relevant and professionally toned descriptions.
 * Structure the Input: Clearly define how the user will provide the database metadata. Using placeholders like [TABLE_NAME], [COLUMN_NAME], and [VALUES] helps in creating a reusable template.
 * Specify the Output Format: To ensure consistency, detail the exact format for the output. Using a structured format like Markdown with clear headings for each table and field is highly effective.
 * Include Examples (Few-Shot Prompting): Providing an example of the expected input and the desired output is one of the most effective ways to guide the AI. This helps in clarifying the expected level of detail and the format.
 * Handle Ambiguity and Edge Cases: Instruct the AI on how to handle situations where a value's meaning might be ambiguous or if a field has a very large number of unique values. For instance, you can instruct it to group similar values or to state when a description is inferred.
A Comprehensive Prompt Template
Here is a prompt template that incorporates the principles mentioned above. You can adapt this template to your specific needs.
The Prompt:
**Persona:** You are a Senior Data Analyst. Your task is to analyze the provided database metadata and generate clear, concise, and human-readable descriptions for every possible value within each field of the tables.

**Objective:** For each table and each of its columns, analyze the provided list of unique values and write a brief description for what each value represents.

**Input Metadata:**

The database metadata will be provided in the following format:

* **Table:** `[TABLE_NAME]`
    * **Column:** `[COLUMN_NAME]`
    * **Data Type:** `[DATA_TYPE]`
    * **Unique Values:** `[LIST_OF_UNIQUE_VALUES]`

**Instructions:**

1.  For each table and column provided, carefully examine the list of unique values.
2.  For each unique value, provide a concise and clear description of what it represents in the context of the column and table.
3.  If the meaning of a value is ambiguous, use your analytical skills to infer its most likely meaning and explicitly state that the description is an inference.
4.  If a column has a large number of unique values that follow a pattern (e.g., numerical ranges, dates), you can describe the pattern rather than each individual value.
5.  Present the output in a clear, well-structured Markdown format as specified below.

**Desired Output Format:**

### `[TABLE_NAME]`

#### `[COLUMN_NAME]`

* **`[Value_1]`**: [Description of Value_1]
* **`[Value_2]`**: [Description of Value_2]
* ...

---

**Example:**

**Input Metadata:**

* **Table:** `Orders`
    * **Column:** `status`
    * **Data Type:** `VARCHAR`
    * **Unique Values:** `['pending', 'shipped', 'delivered', 'cancelled']`
    * **Column:** `priority`
    * **Data Type:** `INTEGER`
    * **Unique Values:** `[1, 2, 3]`

**Desired Output:**

### Orders

#### status

* **pending**: The order has been placed but has not yet been processed for shipping.
* **shipped**: The order has been packaged and sent out for delivery.
* **delivered**: The order has been successfully delivered to the customer.
* **cancelled**: The order has been cancelled by the customer or the system.

#### priority

* **1**: High priority order, requires immediate attention.
* **2**: Medium priority order, to be processed after high priority orders.
* **3**: Low priority order, to be processed when resources are available.

---

**Now, please analyze the following database metadata and generate the descriptions accordingly:**

[Paste the user's database metadata here]

How to Use the Prompt
 * Copy the Template: Start with the provided prompt template.
 * Populate the Metadata: Replace the placeholder [Paste the user's database metadata here] with the actual metadata from the user's database. Ensure the metadata follows the structured format defined in the prompt.
 * Submit to the AI: Provide the complete prompt to the AI.
By using this structured and detailed prompt, you will guide the AI to produce accurate and well-formatted descriptions for all the values in the user's database, making the metadata much easier to understand and use.
