// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ChatbotInteractionContract {
    address public owner;
    
    // Struct to represent a chatbot interaction
    struct ChatbotInteraction {
        uint timestamp;
        address user;
        string interactionData;
        bytes32 encryptedInteractionData;
    }
    
    // An array to store chatbot interactions
    ChatbotInteraction[] public chatbotInteractions;
    
    // Mapping to store user permissions
    mapping(address => bool) public authorizedUsers;

    // Events to log interactions and permission changes
    event InteractionAdded(uint indexed interactionIndex, address indexed user, string interactionData);
    event UserAuthorized(address indexed user);
    event UserRevoked(address indexed user);

    constructor() {
        owner = msg.sender;
    }

    // Modifier to restrict access to authorized users
    modifier onlyAuthorized() {
        require(authorizedUsers[msg.sender] == true, "Not authorized to perform this action");
        _;
    }

    // Add an interaction to the contract
    function addInteraction(bytes32 _encryptedInteractionData) public onlyAuthorized {
        ChatbotInteraction memory newInteraction;
        newInteraction.timestamp = block.timestamp;
        newInteraction.user = msg.sender;
        newInteraction.encryptedInteractionData = _encryptedInteractionData;

        chatbotInteractions.push(newInteraction);

        emit InteractionAdded(chatbotInteractions.length - 1, msg.sender, "Encrypted Data");
    }

    // Get the total number of interactions
    function getInteractionCount() public view returns (uint) {
        return chatbotInteractions.length;
    }

    // Get interaction details by index
    function getInteraction(uint _index) public view returns (uint, address, string memory) {
        require(_index < chatbotInteractions.length, "Interaction index out of bounds");
        ChatbotInteraction memory interaction = chatbotInteractions[_index];
        return (interaction.timestamp, interaction.user, interaction.interactionData);
    }

    // Authorize a user to add interactions
    function authorizeUser(address _user) public {
        require(msg.sender == owner, "Only the owner can authorize users");
        authorizedUsers[_user] = true;
        emit UserAuthorized(_user);
    }

    // Revoke a user's authorization to add interactions
    function revokeUser(address _user) public {
        require(msg.sender == owner, "Only the owner can revoke user authorization");
        authorizedUsers[_user] = false;
        emit UserRevoked(_user);
    }
}
