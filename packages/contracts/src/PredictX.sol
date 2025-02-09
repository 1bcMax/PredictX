// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract PredictX is ReentrancyGuard, Ownable {
    struct Prediction {
        uint256 id;
        address predictor;
        string asset;
        uint256 predictedPrice;
        uint256 predictionTime;
        uint256 settlementTime;
        uint256 totalStaked;
        bool isSettled;
        bool isAI;
    }

    struct Stake {
        address staker;
        uint256 amount;
        bool supportAI;
    }

    mapping(uint256 => Prediction) public predictions;
    mapping(uint256 => mapping(address => Stake)) public stakes;
    
    uint256 public predictionCount;
    uint256 public constant PREDICTION_DURATION = 24 hours;
    uint256 public constant MIN_STAKE_AMOUNT = 0.01 ether;
    
    event PredictionCreated(
        uint256 indexed id,
        address predictor,
        string asset,
        uint256 predictedPrice,
        bool isAI
    );
    
    event StakeAdded(
        uint256 indexed predictionId,
        address indexed staker,
        uint256 amount,
        bool supportAI
    );
    
    event PredictionSettled(
        uint256 indexed id,
        uint256 actualPrice,
        uint256 totalRewards
    );

    constructor() {
        predictionCount = 0;
    }

    function createPrediction(
        string memory asset,
        uint256 predictedPrice,
        bool isAI
    ) external returns (uint256) {
        require(predictedPrice > 0, "Invalid price");
        
        uint256 predictionId = ++predictionCount;
        
        predictions[predictionId] = Prediction({
            id: predictionId,
            predictor: msg.sender,
            asset: asset,
            predictedPrice: predictedPrice,
            predictionTime: block.timestamp,
            settlementTime: block.timestamp + PREDICTION_DURATION,
            totalStaked: 0,
            isSettled: false,
            isAI: isAI
        });

        emit PredictionCreated(
            predictionId,
            msg.sender,
            asset,
            predictedPrice,
            isAI
        );

        return predictionId;
    }

    function stake(uint256 predictionId, bool supportAI) external payable nonReentrant {
        require(msg.value >= MIN_STAKE_AMOUNT, "Stake too small");
        require(predictions[predictionId].id != 0, "Prediction not found");
        require(!predictions[predictionId].isSettled, "Already settled");
        require(
            block.timestamp < predictions[predictionId].settlementTime,
            "Prediction expired"
        );

        stakes[predictionId][msg.sender] = Stake({
            staker: msg.sender,
            amount: msg.value,
            supportAI: supportAI
        });

        predictions[predictionId].totalStaked += msg.value;

        emit StakeAdded(predictionId, msg.sender, msg.value, supportAI);
    }

    function settlePrediction(uint256 predictionId, uint256 actualPrice) external onlyOwner {
        Prediction storage prediction = predictions[predictionId];
        require(prediction.id != 0, "Prediction not found");
        require(!prediction.isSettled, "Already settled");
        require(
            block.timestamp >= prediction.settlementTime,
            "Too early to settle"
        );

        prediction.isSettled = true;

        // Calculate rewards based on prediction accuracy
        uint256 accuracy = calculateAccuracy(prediction.predictedPrice, actualPrice);
        distributeRewards(predictionId, accuracy);

        emit PredictionSettled(predictionId, actualPrice, prediction.totalStaked);
    }

    function calculateAccuracy(uint256 predicted, uint256 actual) 
        internal 
        pure 
        returns (uint256)
    {
        if (predicted > actual) {
            return ((1000 - ((predicted - actual) * 1000 / actual)));
        } else {
            return ((1000 - ((actual - predicted) * 1000 / actual)));
        }
    }

    function distributeRewards(uint256 predictionId, uint256 accuracy) internal {
        Prediction storage prediction = predictions[predictionId];
        
        // Winners are those who:
        // - Supported AI if AI was accurate (accuracy > 900)
        // - Opposed AI if AI was inaccurate (accuracy <= 900)
        bool aiWon = accuracy > 900;
        
        uint256 totalWinningStake;
        mapping(address => Stake) storage predictionStakes = stakes[predictionId];
        
        // Calculate total winning stake
        for (uint i = 0; i < prediction.totalStaked; i++) {
            if (predictionStakes[address(uint160(i))].supportAI == aiWon) {
                totalWinningStake += predictionStakes[address(uint160(i))].amount;
            }
        }
        
        // Distribute rewards
        if (totalWinningStake > 0) {
            for (uint i = 0; i < prediction.totalStaked; i++) {
                address staker = address(uint160(i));
                Stake storage userStake = predictionStakes[staker];
                
                if (userStake.supportAI == aiWon) {
                    uint256 reward = (userStake.amount * prediction.totalStaked) / totalWinningStake;
                    payable(staker).transfer(reward);
                }
            }
        }
    }

    // Fallback function to accept ETH transfers
    receive() external payable {}
}