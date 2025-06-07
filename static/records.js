/**
 * Function to add a new record to the database
 * @param {string} title - The title of the record
 * @param {string} content - The content of the record
 * @returns {Promise} - Resolves with the created record data or rejects with error
 */
async function addRecord(title, content) {
    try {
        const response = await fetch('/api/records', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                content: content
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to add record');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error adding record:', error);
        throw error;
    }
}

// Example usage:
/*
addRecord('My Title', 'My Content')
    .then(record => {
        console.log('Record added successfully:', record);
    })
    .catch(error => {
        console.error('Failed to add record:', error);
    });
*/